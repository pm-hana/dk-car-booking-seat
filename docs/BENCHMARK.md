# 벤치마킹 출처 이력 대장 (Benchmark Attribution Ledger)

DK CAR BOOKING SEAT에 **다른 사람의 아이디어를 참고해 반영한 내역**을 남기는 문서입니다.
남의 결과물을 참고했다면 반드시 여기에 **누구의 / 어떤 출품작의 / 어떤 내용을** 참고했는지 기록합니다.

- 참고 대상: 사내 AI 컨테스트 **AI Work Booster 2026 — 2차 개선** 출품작
- 최초 작성: 2026-08-06
- 관련 문서: [개선제안_2026-08-06.md](개선제안_2026-08-06.md)

---

## 기록 규칙

1. 아이디어를 **반영하기로 결정한 시점**에 `계획` 상태로 한 줄 추가한다.
2. 실제 코드에 적용하면 `적용`으로 바꾸고 **반영 버전(mmdd ver.N)** 을 적는다.
3. 검토했으나 채택하지 않은 것도 `미채택`으로 남긴다 — 왜 안 했는지가 다음 판단에 쓰인다.
4. 출처 표기는 **이름 + 직책 + 출품작명**까지 적는다. 원문 표현은 인용부호로 함께 남긴다.
5. 코드에도 흔적을 남긴다 — 해당 기능 근처 주석에 한 줄:
   `# [벤치마킹] <이름> "<출품작>" — <참고한 내용>. 상세: docs/BENCHMARK.md`

---

## 출처 목록 (AI Work Booster 2026 · 2차 개선)

| # | 이름 | 소속·직책 | 출품작 |
|---|---|---|---|
| 1 | NGUYỄN VĂN HẢI | FAE Engineer Staff | Daekhon Vina Vision — 실시간 그룹 채팅 + 푸시 알림 + 보안 패치 |
| 2 | Hà Văn Lượng | PM Part Leader | 광학 설계·EXT Tube 계산 & Concept 3D 시뮬레이션 |
| 3 | NGUYỄN TRỌNG CHƯƠNG | FAE Nhân viên | VISION AOI Log Analyzer + Gemini AI |
| 4 | Larry Nguyen | FAE Manager | 창고 관리 + Vision 계산 + 보고서 지원 SW |
| 5 | Nguyễn Huy Hoàng | AE Staff | Button Design 2.0 by Claude Code CLI |
| 6 | NGUYỄN THẾ ANH | AE Engineer | Vision Inspection 보고서 자동화 V2 |
| 7 | Đào Văn Bảo | FAE Leader | K-Pulse KPI 관리 시스템 |
| 8 | Lê Quang Trung | AE Nhân viên | SMART REPORT VER 2 |
| 9 | Nguyễn Hoàng Qúy | AE Nhân viên | 리포트 재구조화·안정화·확장 |
| 10 | TRIEU VAN LINH | AE AM | C# UI 자동 생성 시스템 |
| 11 | Lê Khắc Hưng | AE Leader | Log Analyzer V2 |

---

## 반영 내역

| 항목 | 출처(이름 / 출품작) | 참고한 내용 (원문) | 우리 앱 적용 방식 | 상태 | 반영 버전 |
|---|---|---|---|---|---|
| A-1 XSS 차단 | **NGUYỄN VĂN HẢI** / Daekhon Vina Vision | *"có lỗ hổng XSS"* → *"chống XSS"* — 사내 PWA에서 XSS 구멍을 찾아 패치 | 공통 헬퍼 `esc()` 도입 후 사용자 입력이 HTML/SVG로 나가는 5개 지점에 적용 — 예약 카드 정보칸, 좌석 배치도 이름(SVG text), 좌석 툴팁, 중복 신청 경고, 도착완료 안내, 검색 결과 없음 문구 | **적용** | 0806 ver.1 |
| A-2 PIN 비밀 분리 | **Đào Văn Bảo** / K-Pulse | *"Mật khẩu được lưu không mã hóa"*, *"Khóa cơ sở dữ liệu lộ trong mã trang web"* → bcrypt/scrypt 해싱 | `ADMIN_PIN` 하드코딩 제거 → `st.secrets["admin"]`의 salt+sha256 해시와 `hmac.compare_digest` 비교. 4~8자리 허용, 연속 실패 5회 시 세션 잠금. Secrets 미설정 시 로그인 팝업에 경고 노출 | **적용** | 0806 ver.1 |
| A-2 비밀키 커밋 차단 | **NGUYỄN TRỌNG CHƯƠNG** / AOI Log Analyzer | *"Đã thêm .gitignore chặn commit file *.key và các file cấu hình bí mật"* | 점검 결과 `.gitignore`에 `serviceAccountKey.json`·`.streamlit/secrets.toml`이 이미 포함되어 있어 추가 조치 불필요 | **기충족** | — |
| A-3 서버측 권한 검사 | **Đào Văn Bảo** / K-Pulse | *"Kiểm tra phân quyền được thực hiện trên máy chủ (Server-side), không phụ thuộc vào việc người dùng có ẩn hay vô hiệu hóa nút bấm"* | `owner_gate()` 신설 — 수정·취소·도착완료 3경로 공통. 버튼 노출로 판단하지 않고 **값을 바꾸기 직전에 매번 재검사**. 취소는 즉시 삭제 → 확인 팝업(`cancel_dialog`)으로 변경. 관리자·본인은 통과, 그 외는 신청자 이름 확인 | **적용** | 0806 ver.3 |
| A-4 백업/복원 | **Hà Văn Lượng** / Concept 3D 시뮬레이션 | *"Tính năng Export/Import JSON giúp sao lưu toàn bộ... nút Reset khôi phục ngay trạng thái ban đầu chỉ với 1 click"* | 관리자 '💾 백업·복원' 패널 — 원클릭 JSON 내보내기 / 파일로 복원 / 마지막 초기화·복원 되돌리기. 초기화·복원 직전 상태를 스냅샷으로 자동 보관하고 경고에 삭제 건수 표시. 관리자 영역을 예약 유무와 무관하게 렌더하도록 이동(초기화 직후 되돌리기 접근 불가 결함 해소) | **적용** | 0806 ver.4 |
| A-4 저장 실패 경고 | **Đào Văn Bảo** / K-Pulse | *"Hiển thị cảnh báo khi có lỗi kèm nguyên nhân"*, *"Thao tác xóa không có hiệu lực"* | `save_bookings`가 성공 여부를 반환하고, 실패 시 화면 상단에 경고 배너 표시(기존에는 `except: pass`로 무시돼 사용자가 저장된 줄 알았음) | **적용** | 0806 ver.4 |
| A-5 베트남어 지원 | **Nguyễn Huy Hoàng** / Button Design 2.0 | *"200+ từ khóa song ngữ (Việt/Anh)"* — 사내 도구는 이중언어가 기본 / 컨테스트 플랫폼도 한국어·Tiếng Việt·English 3종 제공 | `TR`에 `"vi"` 사전(99키) 추가 + `LANG_OPTIONS` 매핑 도입으로 토글 3종화. 내부 상태 토큰은 그대로 두어 저장 데이터 무영향. 토글 폭 증가에 맞춰 PC·모바일 간격/글자 조정 | **적용** | 0806 ver.2 |
| B-1 내 이름 기억 | **NGUYỄN THẾ ANH** / Vision Inspection V2 | *"cơ chế bộ nhớ đệm (Session Persistence)... Auto Save/Load mà không cần thao tác thêm"* — 매일 2~3분 설정 시간 100% 제거 | 신청 완료 시 이름·기본 출발지를 브라우저 쿠키(`dk_profile`)에 저장하고 다음부터 폼에 자동 채움. 읽기는 `st.context.cookies`, 쓰기는 1회성 컴포넌트만(상시 브릿지 쓰기 금지 원칙 유지). 공용 PC 대비 체크 해제 시 즉시 삭제 | **적용** | 0806 ver.2 |
| B-2 푸시 알림 | **NGUYỄN VĂN HẢI** / Daekhon Vina Vision | *"Thông báo đẩy (nhận cả khi đóng app)"*, *"không phát sinh chi phí"* / 제약: *"iOS cần 16.4+ và cài PWA vào màn hình chính"*, 구 FCM API 중단 | 기존 PWA 위에 배차 확정·변경·출발 임박 알림. iOS 제약은 안내 문구로 명시 | 계획 | — |
| B-3 승인 + 기한 경고 | **Larry Nguyen** / 창고 관리 SW | *"thêm các chức năng approval, cảnh báo quá hạn trả"* | 신규 신청을 `pending`으로 시작, 관리자 '승인 대기' 패널에서 승인. 출발 30분 이내면 '임박', 시각이 지나면 '초과' 배지(주황/빨강). 대기 요약 배너는 전원에게 노출. 수정 시 재승인 필요. 기존 예약(status 없음)은 승인됨으로 간주해 배포 혼란 방지 | **적용** | 0807 ver.1 |
| B-4 상태 3단계화 | **Nguyễn Hoàng Qúy** / 리포트 재구조화 | *"There are only two states (red/not red)"* → PASS/WARNING/FAIL 3단계 | 좌석 색을 확정(초록)/대기·임박(노랑)/빈자리(회색) 3단계로 | 계획 | — |
| B-5 감사 로그 | **Đào Văn Bảo** / K-Pulse | *"Nhật ký thao tác phục vụ kiểm toán (Audit Log)"* | 취소·수정·도착완료·전체초기화를 **별도 저장소**(Firestore `audit` / `audit.json`)에 적재하고 관리자 화면에 최근 30건 표시. ⚠️ 제안서의 "history 확장"에서 변경 — 엑셀 내보내기가 history를 status 필터 없이 전량 내보내므로 섞으면 탑승 실적 엑셀이 오염됨 | **적용** | 0806 ver.3 |
| C-1 통계 대시보드 | **Lê Quang Trung** / SMART REPORT V2 | *"Lưu trữ sản lượng, tỉ lệ lỗi theo ngày, tháng, năm theo biểu đồ"* | 엑셀 내보내기 팝업에 기간 요약 추가 — 타일 3개(탑승 건수·이용 차량·최다 목적지) + 차량별 / 목적지 TOP5 / 출발 시간대 가로 막대. 막대색은 검증 도구로 선정(다크 대비 3:1↑·밝기 밴드 통과) | **적용** | 0807 ver.1 |
| C-1 필터·빠른 조회 | **Lê Khắc Hưng** / Log Analyzer V2 | *"Bổ sung các tùy chỉnh về biểu đồ, thống kê dữ liệu, Lọc data, truy xuất nhanh chóng"* | 기존 연·월·일 선택에 요약 통계를 붙여, 엑셀을 내려받지 않고도 기간별 수치를 화면에서 바로 확인 | **적용(부분)** | 0807 ver.1 |
| C-1 대시보드 UX | **Nguyễn Hoàng Qúy** / 리포트 재구조화 | *"dashboard, search/filter, progress bar, loading overlay, cancel button"* | 대시보드 형태의 요약 패널 적용. 진행 표시·취소 버튼은 현재 데이터 규모에서 불필요해 보류 | **적용(부분)** | 0807 ver.1 |
| C-2 PDF/PPTX 리포트 | **NGUYỄN TRỌNG CHƯƠNG** / AOI Log Analyzer | *"Xuất báo cáo Excel / PDF / CSV/PPTX"*, *"trình bày sẵn"* | 월간 배차 실적을 보고용 PDF로 출력 | 계획 | — |
| C-3 오전/오후 슬롯 | **NGUYỄN TRỌNG CHƯƠNG** / AOI Log Analyzer | *"Lựa chọn được ca ngày và đêm -> giảm thao tác của kỹ sư vận hành"* | 교대 개념을 오전/오후/종일 배차 슬롯으로 치환 | 계획 | — |
| D-1 모듈 분리 | **Nguyễn Hoàng Qúy** / 리포트 재구조화 | *"The entire logic is contained in a single code-behind file"* → *"Refactor into Models + Services"* | 2,708줄 `app.py`를 저장소·렌더·i18n·UI로 분리 | 계획 | — |
| D-2 자동 테스트 | **NGUYỄN TRỌNG CHƯƠNG**(25/25), **Nguyễn Hoàng Qúy**(71/71), **Đào Văn Bảo**(24건) | 세 출품작 모두 2차 개선에서 자동 테스트 도입 | Streamlit `AppTest`로 신청→저장→취소→도착완료→이력 흐름 고정 | 계획 | — |
| D-2 화면 대조 검증 | **TRIEU VAN LINH** / C# UI 자동 생성 | *"Claude code sẽ chụp lại ảnh màn hình vừa tạo so sánh với bản Design"* | UI 수정 후 스크린샷을 이전 버전과 대조해 회귀 확인 | 계획 | — |
| D-3 데이터 비대 방지 | **NGUYỄN VĂN HẢI** / Daekhon Vina Vision | *"dữ liệu & ảnh lưu không giới hạn gây phình DB, dễ văng app"* | `load_history()` 전체 로드 → 날짜 범위 부분 로드 + 오래된 이력 분리 | 계획 | — |
| D-3 로딩 최적화 | **Lê Khắc Hưng** / Log Analyzer V2 | *"Khi nạp ảnh có độ phân giải cao mất nhiều thời gian và tiêu tốn nhiều tài nguyên máy"* | 좌석 현황 팝업의 이력 조회 지연 개선 | 계획 | — |
| D-4 대비(WCAG) 검증 | **Nguyễn Huy Hoàng** / Button Design 2.0 | *"live WCAG contrast checking"*, *"9 semantic color buckets + 38 brand-accurate colors"* | 차량색 팔레트에 대비비 검증 상수화 (INNOVA 실버·SEDONA 블랙 가독성 반복 수정 해소) | 계획 | — |

---

## 미채택 (검토했으나 반영하지 않음)

| 항목 | 출처 | 사유 |
|---|---|---|
| 완전 오프라인 동작(Offline First) | **Hà Văn Lượng** — *"Ứng dụng chạy độc lập trên trình duyệt nội bộ, không gửi dữ liệu ra máy chủ bên ngoài"* | 배차는 **여러 사람이 같은 좌석을 공유**하는 업무라 중앙 저장소가 필수. 오프라인 단독 실행은 좌석 중복 예약을 막을 수 없어 부적합 |
| 실시간 그룹 채팅 | **NGUYỄN VĂN HẢI** | 배차 앱 범위를 벗어남. 사내에 이미 별도 채널이 있어 중복 |
| 3D 시뮬레이션 / Gemini AI 분석 | **Hà Văn Lượng**, **NGUYỄN TRỌNG CHƯƠNG** | 배차 데이터는 좌석·시간 위주라 AI 분석의 이득이 작고, 외부 API 비용·키 관리 부담이 생김 |
