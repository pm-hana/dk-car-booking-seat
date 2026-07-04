---
name: upgrade
description: Phase-1에서 만든 소스(Antigravity·기타 AI툴 산출물)를 Claude Code CLI로 분석→인터뷰→안정화→버그수정→고도화한다. 사용자가 "고도화 / 업그레이드 / upgrade / nâng cấp / Phase 2 / 소스 개선 / 안정화"를 요청하거나 기존 프로젝트를 열고 개선을 원할 때 사용. DAEKHON VINA machine-vision(C# WinForms, VisionPro/Vidi/OpenCV/YOLO, Python, Web) 대상.
---

# Upgrade Skill — Phase 2 고도화 / Giai đoạn 2

Phase-1 산출물을 **망가뜨리지 않고** 다듬고·안정화하고·확장한다.
Tinh chỉnh, ổn định và mở rộng sản phẩm GĐ1 mà **không làm hỏng phần đang chạy tốt**.

## 0. Golden rules / Nguyên tắc vàng
1. **기능 회귀 금지 / Không làm mất chức năng.** 모든 변경은 요청 또는 검증된 버그에 근거. 기존 스타일 유지.
2. **스냅샷 먼저 / Chụp ảnh trước:** `git init && git add -A && git commit -m "baseline"` (git 없으면 폴더를 `…_backup`으로 복사).
3. **큰 변경은 먼저 물어본다 / Hỏi trước khi làm lớn:** 아키텍처 변경·파일 이름 변경·의존성 추가/업그레이드·데이터 포맷 변경 전 **2~3줄 계획 + 승인**.
4. **🔴 고객 코드·데이터는 클라우드 금지 / Không đưa mã·dữ liệu khách lên cloud** (VisionPro/DYT 원본, recipe, 고객 이미지). 분석 대상은 **본인이 만든 도구 코드만**.
5. **증거로 검증 / Kiểm chứng bằng bằng chứng:** build·run·결과 확인. "되겠지(Chắc chạy được)"는 완료가 아니다.

## 1. The loop / Vòng lặp
모든 단계는 동일 루프: **Prompt(명확한 지시) → Context(상황 전부 제공) → Harness(결과 검증).**

## 2. Workflow / Quy trình (7 phases)

**Phase 1 — 분석 / Phân tích**
- 파일 목록 → 언어/스택, 진입점, 빌드·실행 방법, 외부 의존성(카메라·VisionPro/OpenCV·DB·파일), 데이터 I/O 식별.
- **모든 .md/README/주석 먼저 읽기** — 작성자 의도가 거기 있다. 의도를 한 문단으로 요약하고 확인받기.

**Phase 2 — 의도 파악(대화) / Hiểu ý đồ.** AskUserQuestion으로 인터뷰:
- 이걸 한 문장으로? / Làm gì trong một câu?
- 가장 불편한 점·자주 깨지는 곳? / Chỗ nào khó chịu / hay lỗi?
- 하루가 더 있다면 뭘 추가? / Nếu thêm một ngày, thêm gì?
- 누가·어떤 PC에서 쓰나? / Ai dùng, máy nào?

**Phase 3 — 안정화 / Ổn định.** 깨끗하게 빌드·실행: 컴파일/런타임 오류 수정, I/O·외부호출에 try/catch, null/빈값 가드, 죽은 코드 제거.

**Phase 4 — 버그수정 / Sửa lỗi.** 재현 → 수정 → 재검증(red→green). 진짜 버그는 **수정을 되돌려 다시 실패하는지** 확인해 증명.

**Phase 5 — 개선 아이디어(대화) / Ý tưởng cải tiến.** 백로그: Quick wins(UX/검증) · Robustness(에러/로그/설정) · Performance(속도/메모리) · Features("하루 더"). **개발자와 함께** 우선순위.

**Phase 6 — 구현 / Triển khai.** 작고·외과적이고·검증된 변경. 한 번에 한 가지. 논리 단위마다 commit.

**Phase 7 — 검증·보고 / Kiểm chứng·báo cáo.** build/run, Before→After 캡처(시간·줄·에러·속도), 보고서 작성(대회 양식에 사용).

## 3. Language playbooks / Cẩm nang ngôn ngữ
- **C#/WinForms(머신비전):** 카메라/임계값/경로를 config로 외부화 · 무거운 비전 작업을 UI 스레드 밖으로(async/Task) · VisionPro/OpenCV/파일 호출 try/catch · 이미지/핸들 dispose · 간단 로그 추가.
- **Python:** virtualenv + requirements.txt · type hint · `__main__` 가드 · 핫루프 vectorize(numpy) · 파일/네트워크 I/O 가드.
- **HTML/JS/Web:** 시맨틱 마크업 · secret 인라인 금지 · 무거운 핸들러 debounce · 무거운 자원 lazy-load · 기본 a11y·반응형.
- **Java:** 명확한 예외(삼키지 말 것) · 루프/컬렉션 경계 · 가독성 좋은 stream · 단위 점검 추가.

## 4. Performance checklist / Hiệu năng
반복 작업 제거(cache/memoize) · N+1 파일/DB/API 호출 회피(batch/병렬) · UI 반응 유지(async, 메인스레드 차단 금지) · 자원 해제(이미지/핸들/연결) · **전후 측정**.

## 5. 독점 SDK 주의 / Lưu ý SDK độc quyền
VisionPro/Vidi/Cognex 등의 **API를 추측해 지어내지 말 것.** 설치된 SDK의 XML 문서·헤더·샘플을 읽어 확인하고, **시그니처는 반드시 빌드로 검증**. 불확실하면 사용자에게 물어본다.

## 6. 개발자와 대화 / Trao đổi
**상대 언어 사용(VN 직원에겐 베트남어).** 잘 되는 점부터 언급. AI는 **대체가 아니라 강점 증폭기**. 변경은 하나씩 제안하고 선택은 본인이. 동작하는 결과마다 인정·축하.

## 7. Upgrade Report template (대회 제출용)
```
■ 프로젝트 / Dự án:
■ 개발자·부서·트랙 / Tác giả·Phòng·Track (A/B/C/D):
■ 기술스택 / Stack:
■ 한 줄 요약 / Tóm tắt 1 câu:
■ 안정화 / Ổn định:
■ 버그수정 / Sửa lỗi:
■ 기능개선 / Cải tiến:
■ 성능 Before→After / Hiệu năng:  시간 __→__ · 코드·에러 __→__ · 속도·메모리 __→__
■ 사용도구 / Công cụ: Claude Code CLI (+ ...)
■ 데모·스크린샷 / Demo·Ảnh:
■ 다음 단계 / Bước tiếp theo:
```

## Safety / An toàn (요약)
작업 전 git 스냅샷 & 단계마다 commit · 고객 코드·데이터 클라우드 금지(미승인) · 큰 변경 전 확인 · build/run으로 검증 · 기존 동작 보존.
