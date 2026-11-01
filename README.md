# 리눅스 및 도커 웹 서버 구축 과제

## 1단계: 개발 환경 세팅
- OS: Windows + WSL2 (Ubuntu)
- 사용 도구: VS Code, 터미널

## 2단계: 도커(Docker) 설치 및 확인
- 도커 엔진 설치 완료
- `sudo docker info` 실행 결과 정상 확인

## 3단계: 나만의 웹 서버(Container) 띄우기
- `index.html` 및 `Dockerfile` 작성 완료
- `my-web-server` 이미지 빌드 완료
- 포트 8080을 통해 "Hello, Docker World!" 웹페이지 접속 성공