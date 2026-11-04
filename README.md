# 개발 워크스테이션 구축 실습

## 1. 프로젝트 개요

본 과제는 로컬 개발 환경에서 코드가 재현 가능하게 실행되고 배포될 수 있도록 핵심 도구인 리눅스 터미널(CLI), Docker(컨테이너), Git/GitHub(버전 관리)를 세팅하고 다루는 방법을 익히는 것을 목표로 합니다. 나만의 웹 서버를 컨테이너화하고 포트 매핑, 볼륨 마운트 등을 직접 검증하여 격리된 실행 환경의 구조적 원칙을 이해합니다.

## 2. 실행 환경

* **OS:** Windows + WSL2 (Ubuntu 22.04) / PowerShell
* **Shell:** bash (WSL) / pwsh (Windows)
* **Docker:** Docker version 29.9.2, build a82e528 (OrbStack / Docker Desktop 연동)
* **Git:** Git version 2.x

## 3. 수행 체크리스트

* [x] 터미널 기본 조작 및 폴더 구성
* [x] 권한 변경 실습 (파일 1개, 디렉토리 1개)
* [x] Docker 설치 및 데몬 점검
* [x] hello-world 및 ubuntu 컨테이너 실행 실습
* [x] Dockerfile 기반 커스텀 웹 서버 빌드 및 실행
* [x] 포트 매핑 및 브라우저 접속 검증
* [ ] 바인드 마운트 변경 반영 검증 (추가 필요)
* [x] Docker 볼륨 생성 및 데이터 영속성 검증
* [x] Git 사용자 설정 및 VSCode GitHub 연동

## 4. 상세 수행 로그 및 검증 방법

### 4.1 터미널 조작 및 권한 실습

**1) 터미널 기본 조작 (위치 확인, 이동, 복사, 삭제 등)**
```bash
# 아래 명령어들을 터미널에서 순서대로 치고 전체 결과를 여기에 복붙해주세요!
# pwd
# ls -la
# cp test.txt copy_test.txt
# mv copy_test.txt moved_test.txt
# rm moved_test.txt
[여기에 기본 조작 명령어 실행 결과 붙여넣기]
```

**2) 파일 권한 변경 전/후 비교**
```bash
docker-desktop:/tmp/docker-desktop-root/run/desktop/mnt/host/c/Users/User/E-1-1-# mkdir -p ~/mission-practice
docker-desktop:/tmp/docker-desktop-root/run/desktop/mnt/host/c/Users/User/E-1-1-# cd ~/mission-practice
docker-desktop:~/mission-practice# touch test.txt
docker-desktop:~/mission-practice# ls -l test.txt
-rw-r--r--    1 root     root             0 Nov  2 09:27 test.txt
docker-desktop:~/mission-practice# chmod 755 test.txt
docker-desktop:~/mission-practice# ls -l test.txt
-rwxr-xr-x    1 root     root             0 Nov  2 09:27 test.txt
docker-desktop:~/mission-practice# exit
```

### 4.2 Docker 설치 및 기본 점검

**1) 설치 버전 및 데몬 상태 확인**
```bash
PS C:\Users\User\E-1-1-> docker --version
Docker version 29.9.2, build a82e528

# 터미널에 docker info 를 치고 나오는 결과를 아래에 복붙해주세요. (데몬 동작 확인)
[여기에 docker info 결과 붙여넣기]
```

**2) 기본 운영 명령 수행 로그 (images, ps, logs, stats)**
```bash
# 아래 명령어들을 치고 나오는 결과를 복붙해주세요.
# docker images
# docker ps -a
# docker stats --no-stream
[여기에 운영 명령어 실행 결과 붙여넣기]
```

### 4.3 컨테이너 실행 실습

**1) hello-world 및 ubuntu 컨테이너 진입 테스트**
```bash
PS C:\Users\User\E-1-1-> docker run hello-world
Hello from Docker!
This message shows that your installation appears to be working correctly.
To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

PS C:\Users\User\E-1-1-> docker run -it ubuntu bash
root@a768cdd98613:/# ls
bin  dev  home  lib64  mnt  proc  run   srv  tmp  var
boot etc  lib   media  opt  root  sbin  sys  usr
root@a768cdd98613:/# exit
PS C:\Users\User\E-1-1->
```
* **컨테이너 종료/유지 관찰 요약:** `docker run -it`로 진입한 내부 셸에서 `exit`를 입력하면 메인 프로세스가 종료되어 컨테이너가 멈춥니다. 반면, 백그라운드(`-d`)로 실행 중인 컨테이너에 `exec`로 진입했다가 나오면 컨테이너는 계속 유지됩니다.

### 4.4 Dockerfile 기반 커스텀 이미지 제작 및 포트 매핑

* **베이스 이미지:** `nginx:latest`
* **커스텀 목적:** 기본 Nginx 웹 페이지 대신 직접 작성한 `index.html`("Hello, Docker World!")을 출력하도록 정적 콘텐츠 교체

**1) Dockerfile 및 빌드 & 포트 매핑 실행**
```bash
# Dockerfile 내용
FROM nginx:latest
COPY index.html /usr/share/nginx/html/

# 도커 빌드 및 실행 로그
PS C:\Users\User\E-1-1-> docker build -t my-web-server .
PS C:\Users\User\E-1-1-> docker run -d -p 8080:80 --name my-first-server my-web-server
dcf2a0949f45f4325ac9cf5e80d37bb97928f84bb5e8837f4282a8ff57b553ff
```

**2) 브라우저 접속 증거**
*(아래에 접속 성공 화면 스크린샷 캡처본을 첨부합니다. 주소창의 localhost:8080이 보여야 합니다.)*
![포트매핑 접속 스크린샷](screenshot_port_8080.png)

### 4.5 바인드 마운트 및 볼륨 영속성 검증

**1) 바인드 마운트 (호스트 변경 전/후 비교)**
```bash
# 터미널에 아래 명령을 치고 결과를 복붙해주세요!
# mkdir bind-test && echo "host data" > bind-test/hello.txt
# docker run -d --name bind-container -v $(pwd)/bind-test:/app ubuntu sleep infinity
# docker exec -it bind-container cat /app/hello.txt
# echo "changed data" > bind-test/hello.txt
# docker exec -it bind-container cat /app/hello.txt
[여기에 바인드 마운트 실행 결과 붙여넣기]
```

**2) Docker 볼륨 영속성 (컨테이너 삭제 후 데이터 유지 검증)**
```bash
# 볼륨 생성 및 첫 번째 컨테이너에 데이터 기록
PS C:\Users\User\E-1-1-> docker volume create mydata
PS C:\Users\User\E-1-1-> docker run -d --name vol-test -v mydata:/data ubuntu sleep infinity
aae13ef481ae97786ade867d16e34f98ca3b17731b66205a0504357ce04046f2
PS C:\Users\User\E-1-1-> docker exec -it vol-test bash -c "echo hi > /data/hello.txt"
PS C:\Users\User\E-1-1-> docker exec -it vol-test cat /data/hello.txt
hi

# 기존 컨테이너 삭제 후, 새 컨테이너에서 데이터가 유지되었는지 확인 (영속성 검증)
PS C:\Users\User\E-1-1-> docker rm -f vol-test
vol-test
PS C:\Users\User\E-1-1-> docker run -d --name vol-test2 -v mydata:/data ubuntu sleep infinity
f6abeaea9f130640a11aab70968b300127c9fc9606d0605622b8042e7b4b7bb9
PS C:\Users\User\E-1-1-> docker exec -it vol-test2 cat /data/hello.txt
hi
```

### 4.6 Git 설정 및 GitHub 연동

```bash
PS C:\Users\User\E-1-1-> git config --list
user.name=YourName
user.email=YourEmail@example.com
```

**VSCode GitHub 연동 및 푸시 완료 증거**
*(아래에 GitHub 레포지토리에 파일이 올라간 화면 캡처본을 첨부합니다.)*
![GitHub 연동 스크린샷](screenshot_github.png)

## 5. 트러블슈팅 (Troubleshooting)

### 이슈 1: 웹 서버 포트 충돌 문제
* **문제:** `docker run` 실행 시 `port is already allocated` 에러 발생.
* **원인 가설:** 이미 8080 포트를 사용 중인 다른 프로세스나 컨테이너가 있을 것이다.
* **확인:** `docker ps` 명령어를 통해 실행 중인 컨테이너 목록 확인.
* **해결/대안:** 기존에 실행 중이던 컨테이너를 `docker stop` 및 `docker rm`으로 삭제한 후 다시 실행하여 해결함.

### 이슈 2: WSL2 배포판 내부 Docker CLI 실행 에러
* **문제:** `docker run hello-world` 실행 시 "It looks like you have tried to invoke the docker CLI from the docker-desktop WSL2 distribution" 에러 발생.
* **원인 가설:** 리눅스 파일 권한(`chmod`) 실습을 위해 접속했던 내부 도커 시스템(docker-desktop 환경) 안에 여전히 머물러 있어서 명령어가 막힌 것이다.
* **확인:** 터미널 프롬프트 앞부분이 파워셸(`PS C:\...`)이 아닌 `docker-desktop...#` 임을 확인.
* **해결/대안:** 터미널에 `exit` 명령어를 입력해 원래의 윈도우 파워셸 환경으로 빠져나온 뒤, 도커 명령어를 재실행하여 정상 작동을 확인.