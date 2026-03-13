# VM 배포 가이드

## 1. VM에 코드 올리기

```bash
# 로컬에서 실행
gcloud compute scp --recurse /Users/jwlee/Documents/dev/siti_claude_skils/siti-slack-bot \
  VM_NAME:/home/ubuntu/siti-slack-bot \
  --zone ZONE --project PROJECT_ID
```

## 2. VM 접속 후 설정

```bash
# 패키지 설치
cd /home/ubuntu/siti-slack-bot
pip3 install -r requirements.txt

# .env 파일 생성
cp .env.example .env
nano .env  # 실제 값으로 채우기
```

## 3. systemd 서비스 등록 (항상 켜두기)

```bash
sudo nano /etc/systemd/system/siti-slack-bot.service
```

아래 내용 입력:
```ini
[Unit]
Description=시티 데이터탐정 Slack Bot
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/siti-slack-bot
EnvironmentFile=/home/ubuntu/siti-slack-bot/.env
ExecStart=/usr/bin/python3 main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# 서비스 활성화 및 시작
sudo systemctl daemon-reload
sudo systemctl enable siti-slack-bot
sudo systemctl start siti-slack-bot

# 상태 확인
sudo systemctl status siti-slack-bot

# 로그 확인
journalctl -u siti-slack-bot -f
```

## 4. Slack App 설정

### Socket Mode 활성화
- api.slack.com → 앱 선택 → Socket Mode → Enable
- App-Level Token 생성 (scope: connections:write) → SLACK_APP_TOKEN에 입력

### Event Subscriptions
- Event Subscriptions → Enable
- Subscribe to bot events:
  - `app_mention`
  - `message.im`

### 봇을 채널에 초대
```
/invite @시티_데이터탐정
```
