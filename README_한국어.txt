영원 ETERNITY 모집 사이트 - 실행 방법

구성 파일
- index.html: 밝은 아이보리/골드, 둥근 모서리 모집 페이지
- app.py: 지원서 제출 API. 담당자 Discord DM으로 전송
- requirements.txt: Python 패키지 목록
- .env.example: 환경 변수 예시

실행 방법 (Windows)
1. Python이 설치된 컴퓨터에서 이 폴더를 엽니다.
2. 터미널에서 다음 명령어를 실행합니다.
   py -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
3. .env.example 파일을 복사하고 이름을 .env 로 바꿉니다.
4. .env 파일에서 DISCORD_BOT_TOKEN= 뒤에 Discord Developer Portal의 봇 토큰을 입력합니다.
   토큰을 다른 사람에게 보내거나 index.html에 넣지 마세요.
5. 실행:
   py app.py
6. 브라우저에서 http://127.0.0.1:5000 을 엽니다.

중요
- 웹사이트를 다른 사람도 사용하려면 HTTPS가 지원되는 서버에 app.py를 배포해야 합니다.
- Discord 봇 토큰은 서버 환경 변수로 안전하게 관리하세요.
- 담당자 사용자 ID는 1559815109071732808로 설정되어 있습니다.
- 봇이 담당자에게 DM을 보낼 수 있어야 합니다. 담당자와 봇이 같은 서버에 있고,
  디스코드의 DM/개인정보 설정이 허용되어 있는지 확인하세요.
- 이 예제는 제출 내용을 데이터베이스에 저장하지 않습니다.
- 기존 봇과 같은 토큰을 써도 되지만, 기존 봇을 별도로 실행하는 방식은 유지할 수 있습니다.
- 실제 공개 서비스에서는 HTTPS, 스팸 방지, 접근 로그 및 운영 정책을 확인하세요.
