"""시티 데이터탐정 Slack Bot — Socket Mode"""

import logging
import os
import time

from pathlib import Path

from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from usage_logger import log_usage

load_dotenv(Path(__file__).parent / ".env", override=True)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = App(token=os.environ["SLACK_BOT_TOKEN"])


@app.event("app_mention")
def handle_mention(event, say, client):
    """봇 멘션 처리"""
    # 멘션 텍스트에서 봇 ID 제거
    text = event.get("text", "")
    user = event.get("user", "")
    channel = event.get("channel", "")
    thread_ts = event.get("thread_ts") or event.get("ts")

    # <@BOTID> 부분 제거
    import re
    question = re.sub(r"<@[A-Z0-9]+>", "", text).strip()

    if not question:
        say(text="안녕하세요! 시티 데이터에 대해 무엇이든 물어보세요 😊", thread_ts=thread_ts)
        return

    # 처리 중 메시지
    say(text="🔎 빠르게 데이터를 찾아올게요!", thread_ts=thread_ts)

    start = time.time()
    try:
        from agent import ask
        answer = ask(question)
        say(text=answer, thread_ts=thread_ts)
    except Exception as e:
        logger.exception("에이전트 오류")
        answer = f"❌ 오류가 발생했습니다: {str(e)}"
        say(text=answer, thread_ts=thread_ts)
    finally:
        duration_ms = int((time.time() - start) * 1000)
        log_usage(
            user_id=user,
            channel=channel,
            channel_type="channel",
            question=question,
            answer=answer,
            duration_ms=duration_ms,
        )


@app.event("message")
def handle_dm(event, say):
    """DM 처리 (봇과의 1:1 대화)"""
    # 봇 자신의 메시지는 무시
    if event.get("bot_id"):
        return
    # 채널 메시지(서브타입 없는 DM만 처리)
    if event.get("channel_type") != "im":
        return

    question = event.get("text", "").strip()
    if not question:
        return

    user = event.get("user", "")
    channel = event.get("channel", "")

    start = time.time()
    try:
        from agent import ask
        say(text="🔎 빠르게 데이터를 찾아올게요!")
        answer = ask(question)
        say(text=answer)
    except Exception as e:
        logger.exception("에이전트 오류")
        answer = f"❌ 오류가 발생했습니다: {str(e)}"
        say(text=answer)
    finally:
        duration_ms = int((time.time() - start) * 1000)
        log_usage(
            user_id=user,
            channel=channel,
            channel_type="dm",
            question=question,
            answer=answer,
            duration_ms=duration_ms,
        )


if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    logger.info("시티 데이터탐정 봇 시작!")
    handler.start()
