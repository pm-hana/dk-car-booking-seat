// DK CAR BOOKING PWA 서비스워커 — '설치 가능(installable)' 조건 충족용 최소 구현.
// (Streamlit은 루트 스코프 SW를 못 올려서, /app/static/ 스코프에서 런처 페이지 app.html을 제어한다.)
self.addEventListener('install', () => self.skipWaiting());
self.addEventListener('activate', (e) => e.waitUntil(self.clients.claim()));
// fetch 핸들러가 '존재'해야 크롬이 설치 가능으로 인식. 네트워크는 그대로 통과시킨다.
self.addEventListener('fetch', () => {});
