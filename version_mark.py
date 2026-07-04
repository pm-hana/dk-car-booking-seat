#!/usr/bin/env python
"""Claude Code PostToolUse 훅.
Claude Code가 app.py를 Edit/Write 하면 '증가 대기' 표시(.version_pending)를 남긴다.
실제 버전 증가는 턴 종료 시 version_bump.py(Stop 훅)가 이 표시를 보고 1회만 수행한다.
(한 작업에서 app.py를 여러 번 고쳐도 표시는 하나 → 버전은 1만 증가)
"""
import sys
import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MARKER = os.path.join(BASE_DIR, ".version_pending")


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        return  # 입력을 못 읽어도 훅은 조용히 종료(작업 방해 금지)

    tool_input = payload.get("tool_input", {}) or {}
    file_path = tool_input.get("file_path", "") or ""

    # 편집 대상이 app.py 일 때만 증가 대기 표시
    if os.path.basename(file_path).lower() == "app.py":
        try:
            with open(MARKER, "w", encoding="utf-8") as f:
                f.write("pending")
        except Exception:
            pass


if __name__ == "__main__":
    main()
