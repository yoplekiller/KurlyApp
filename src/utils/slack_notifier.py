from datetime import datetime

import requests

from config.app_config import AppConfig
from utils.logger import get_logger

logger = get_logger(__name__)


def send_failure_alert(test_name: str, error_summary: str, ai_analysis: str) -> None:
    if not AppConfig.SLACK_WEBHOOK_URL:
        logger.warning("Slack 알림 스킵: SLACK_WEBHOOK_URL 미설정")
        return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    payload = {
        "blocks": [
            {
                "type": "header",
                "text": {"type": "plain_text", "text": "🔴 테스트 실패 알림"},
            },
            {
                "type": "section",
                "fields": [
                    {"type": "mrkdwn", "text": f"*테스트명*\n`{test_name}`"},
                    {"type": "mrkdwn", "text": f"*발생 시각*\n{timestamp}"},
                ],
            },
            {"type": "divider"},
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*에러 요약*\n```{error_summary[:300]}```",
                },
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*🤖 AI 분석*\n{ai_analysis}",
                },
            },
        ]
    }

    try:
        resp = requests.post(AppConfig.SLACK_WEBHOOK_URL, json=payload, timeout=10)
        resp.raise_for_status()
        logger.info("Slack 알림 전송 완료: %s", test_name)
    except requests.RequestException as e:
        logger.warning("Slack 알림 전송 실패: %s", e)
