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
| A-3 서버측 권한 검사 | **Đào Văn Bảo** / K-Pulse | *"Kiểm tra phân quyền được thực hiện trên máy chủ (Server-side), không phụ thuộc vào việc người dùng có ẩn hay vô hiệu hóa nút bấm"* | 예약 취소·수정 시 본인 확인 → 버튼 노출이 아니라 저장 직전에 검사 | 계획 | — |
| A-4 백업/복원 | **Hà Văn Lượng** / Concept 3D 시뮬레이션 | *"Tính năng Export/Import JSON giúp sao lưu toàn bộ... nút Reset khôi phục ngay trạng thái ban đầu chỉ với 1 click"* | 관리자 화면에 예약 JSON 원클릭 백업·복원, 전체 초기화 전 자동 스냅샷 | 계획 | — |
| A-4 저장 실패 경고 | **Đào Văn Bảo** / K-Pulse | *"Hiển thị cảnh báo khi có lỗi kèm nguyên nhân"*, *"Thao tác xóa không có hiệu lực"* | `save_bookings`의 조용한 `except: pass` → 사용자에게 실패 표시 | 계획 | — |
| A-5 베트남어 지원 | **Nguyễn Huy Hoàng** / Button Design 2.0 | *"200+ từ khóa song ngữ (Việt/Anh)"* — 사내 도구는 이중언어가 기본 / 컨테스트 플랫폼도 한국어·Tiếng Việt·English 3종 제공 | `TR` 사전에 `"vi"` 추가, 언어 토글 3종으로 확장 | 계획 | — |
| B-1 내 이름 기억 | **NGUYỄN THẾ ANH** / Vision Inspection V2 | *"cơ chế bộ nhớ đệm (Session Persistence)... Auto Save/Load mà không cần thao tác thêm"* — 매일 2~3분 설정 시간 100% 제거 | 기존 관리자 로그인 유지용 localStorage 브릿지를 재사용해 신청자 이름·기본 출발지 자동 채움 | 계획 | — |
| B-2 푸시 알림 | **NGUYỄN VĂN HẢI** / Daekhon Vina Vision | *"Thông báo đẩy (nhận cả khi đóng app)"*, *"không phát sinh chi phí"* / 제약: *"iOS cần 16.4+ và cài PWA vào màn hình chính"*, 구 FCM API 중단 | 기존 PWA 위에 배차 확정·변경·출발 임박 알림. iOS 제약은 안내 문구로 명시 | 계획 | — |
| B-3 승인 + 기한 경고 | **Larry Nguyen** / 창고 관리 SW | *"thêm các chức năng approval, cảnh báo quá hạn trả"* | `신청 → 승인 → 탑승 → 완료` 상태 + 출발 임박 미승인 경고 | 계획 | — |
| B-4 상태 3단계화 | **Nguyễn Hoàng Qúy** / 리포트 재구조화 | *"There are only two states (red/not red)"* → PASS/WARNING/FAIL 3단계 | 좌석 색을 확정(초록)/대기·임박(노랑)/빈자리(회색) 3단계로 | 계획 | — |
| B-5 감사 로그 | **Đào Văn Bảo** / K-Pulse | *"Nhật ký thao tác phục vụ kiểm toán (Audit Log)"* | `history`에 `완료`뿐 아니라 `취소`·`수정`·`관리자 초기화`도 적재 | 계획 | — |
| C-1 통계 대시보드 | **Lê Quang Trung** / SMART REPORT V2 | *"Lưu trữ sản lượng, tỉ lệ lỗi theo ngày, tháng, năm theo biểu đồ"* | 엑셀 내보내기 팝업에 월/일 통계 + 차트 | 계획 | — |
| C-1 필터·빠른 조회 | **Lê Khắc Hưng** / Log Analyzer V2 | *"Bổ sung các tùy chỉnh về biểu đồ, thống kê dữ liệu, Lọc data, truy xuất nhanh chóng"* | 이력 조회에 차량·목적지·기간 필터 | 계획 | — |
| C-1 대시보드 UX | **Nguyễn Hoàng Qúy** / 리포트 재구조화 | *"dashboard, search/filter, progress bar, loading overlay, cancel button"* | 대용량 이력 조회 시 진행 표시·취소 | 계획 | — |
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
