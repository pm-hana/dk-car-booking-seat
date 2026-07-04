#!/usr/bin/env python
"""Claude Code Stop 훅.
Claude Code 턴이 끝날 때 실행된다. version_mark.py가 남긴 '증가 대기' 표시
(.version_pending)가 있으면 → 버전을 1 증가시키고 VER 백업을 만든 뒤 표시를 지운다.
표시가 없으면(=이번 턴에 app.py 코드 작업이 없었으면) 아무것도 하지 않는다.

버전 규칙:
  - 같은 날: count = max(저장 count, VER/mmdd 실제 최대번호) + 1  (되감김 없이 단조 증가)
  - 날짜가 바뀐 첫 작업: 그날 mmdd 로 새로 시작(보통 ver.1)
"""
import os
import re
import csv
import json
import shutil
import datetime
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MARKER = os.path.join(BASE_DIR, ".version_pending")
NOTE_FILE = os.path.join(BASE_DIR, ".version_note")   # Claude Code가 남긴 이번 버전 완료 내용(항목별 줄바꿈)
COUNTER_FILE = os.path.join(BASE_DIR, "version_counter.json")
APP_FILE = os.path.join(BASE_DIR, "app.py")
VER_DIR = os.path.join(BASE_DIR, "VER")


def load_counter():
    if os.path.exists(COUNTER_FILE):
        try:
            with open(COUNTER_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def max_backup_count(display_date):
    """VER/{mmdd} 폴더의 app_ver_N.py 중 가장 큰 N(없으면 0).
    JSON이 유실·손상돼도 실제 백업에서 차수를 복구해 번호 재사용을 막는다."""
    try:
        d = os.path.join(VER_DIR, display_date)
        if not os.path.isdir(d):
            return 0
        mx = 0
        for fn in os.listdir(d):
            m = re.match(r"app_ver_(\d+)\.py$", fn)
            if m:
                mx = max(mx, int(m.group(1)))
        return mx
    except Exception:
        return 0


def _clear_note():
    """이번 버전에 소비한 완료 내용 노트를 삭제(다음 버전이 이전 내용을 재사용하지 않도록)."""
    try:
        if os.path.exists(NOTE_FILE):
            os.remove(NOTE_FILE)
    except Exception:
        pass


def append_version_log(display_date, count, now):
    """버전별 완료 내용을 VER/{mmdd}/{mmdd}_버전별_완료내용.csv 에 한 줄 자동 추가한다.
    - 완료 내용은 .version_note(Claude Code가 이번 턴에 남긴 항목별 줄바꿈 텍스트)에서 읽는다.
      CSV 셀 안에서도 줄바꿈이 그대로 보존되어(자동 따옴표 처리) 항목별로 가시성 있게 표시된다.
    - 노트가 없으면 '(완료 내용 미기재)'로 대체하고, 같은 버전 줄이 이미 있으면 중복 추가하지 않는다.
    - VER/ 는 .gitignore 대상이라 이 CSV는 로컬 문서로만 유지된다(배포/커밋 안 됨).
    실패해도 훅을 절대 죽이지 않는다."""
    try:
        day_dir = os.path.join(VER_DIR, display_date)
        os.makedirs(day_dir, exist_ok=True)
        csv_path = os.path.join(day_dir, f"{display_date}_버전별_완료내용.csv")
        ver_label = f"ver.{count}"

        # 완료 내용: Claude Code가 남긴 노트(없으면 미기재)
        note = ""
        if os.path.exists(NOTE_FILE):
            try:
                with open(NOTE_FILE, "r", encoding="utf-8") as f:
                    note = f.read().strip()
            except Exception:
                note = ""
        if not note:
            note = "(완료 내용 미기재)"

        # 같은 버전 줄이 이미 있으면 중복 추가 방지 ('ver.N,' 은 항상 1열 맨 앞·따옴표 없음)
        if os.path.exists(csv_path):
            try:
                with open(csv_path, "r", encoding="utf-8-sig") as f:
                    if (ver_label + ",") in f.read():
                        _clear_note()
                        return
            except Exception:
                pass

        new_file = not os.path.exists(csv_path)
        # 새 파일이면 Excel 한글 대비 BOM 포함(utf-8-sig)으로 헤더부터, 아니면 그대로 이어붙임
        enc = "utf-8-sig" if new_file else "utf-8"
        with open(csv_path, "a", encoding=enc, newline="") as f:
            w = csv.writer(f)
            if new_file:
                w.writerow(["버전", "일시", "완료 내용 (Claude Code)"])
            w.writerow([ver_label, f"{display_date} {now.strftime('%H:%M')}", note])

        _clear_note()
    except Exception:
        pass


def git(*args, timeout=60):
    """BASE_DIR에서 git 명령 실행. (returncode, stdout+stderr) 반환. 실패해도 예외 안 냄."""
    try:
        p = subprocess.run(
            ["git", *args],
            cwd=BASE_DIR,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return p.returncode, (p.stdout or "") + (p.stderr or "")
    except Exception as e:
        return 1, str(e)


def auto_deploy(display_date, count):
    """버전이 오른 턴에 한해 변경사항을 자동 커밋 + push 하여 Streamlit 배포판을 즉시 갱신.
    실패(오프라인·인증 등)해도 훅을 죽이지 않는다. 로컬 커밋은 남으므로 다음 성공 push가 따라잡는다.
    안전장치: 현재 브랜치가 main일 때만 push 한다."""
    # 현재 브랜치 확인 (main 이 아니면 자동 push 하지 않음)
    rc, branch = git("rev-parse", "--abbrev-ref", "HEAD")
    if rc != 0 or branch.strip() != "main":
        return

    # 스테이징 (.gitignore가 VER/·bookings.json 등 로컬 전용 파일을 걸러줌)
    git("add", "-A")

    # 스테이징된 변경이 없으면 커밋 생략 (--quiet: 변경 있으면 0, 없으면 1)
    rc, _ = git("diff", "--cached", "--quiet")
    if rc == 0:
        # 커밋할 게 없어도 원격이 뒤처져 있을 수 있으니 push 는 시도
        git("push", "origin", "main")
        return

    git("commit", "-m", f"auto-deploy: {display_date} ver.{count} (app.py 자동 배포)")
    git("push", "origin", "main")


def main():
    # 증가 대기 표시가 없으면 종료 (app.py 코드 작업이 없었던 턴)
    if not os.path.exists(MARKER):
        return

    now = datetime.datetime.now()
    today = now.strftime("%Y-%m-%d")
    display_date = now.strftime("%m%d")

    data = load_counter()
    if data.get("date", "") == today:
        base = max(int(data.get("count", 0) or 0), max_backup_count(display_date))
    else:
        base = max_backup_count(display_date)  # 날짜가 바뀐 첫 작업 → 새로 시작
    count = base + 1

    try:
        with open(COUNTER_FILE, "w", encoding="utf-8") as f:
            json.dump({"date": today, "count": count}, f, ensure_ascii=False, indent=4)
    except Exception:
        pass

    # VER/[mmdd]/app_ver_N.py 백업 (count가 항상 최대+1이라 덮어쓰기 없음)
    try:
        backup_dir = os.path.join(VER_DIR, display_date)
        os.makedirs(backup_dir, exist_ok=True)
        if os.path.exists(APP_FILE):
            shutil.copy2(APP_FILE, os.path.join(backup_dir, f"app_ver_{count}.py"))
    except Exception:
        pass

    # 버전별 완료 내용 CSV에 이번 버전 줄 자동 추가(.version_note 소비 후 삭제)
    try:
        append_version_log(display_date, count, now)
    except Exception:
        pass

    # 표시 제거 (다음 턴에서 다시 코드 작업이 있어야 재증가)
    try:
        os.remove(MARKER)
    except Exception:
        pass

    # 버전이 올랐으니 변경사항을 자동 커밋 + push → Streamlit 배포판 즉시 갱신
    try:
        auto_deploy(display_date, count)
    except Exception:
        pass


if __name__ == "__main__":
    main()
