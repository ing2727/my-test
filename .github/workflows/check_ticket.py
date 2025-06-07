import requests
from bs4 import BeautifulSoup
import os

# 🔐 Slack Webhook URL (GitHub Secrets에 SLACK_WEBHOOK_URL로 등록하세요)
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

# 🎫 멜론티켓 공연 상세 URL (원하는 공연 링크로 변경하세요)
MELON_TICKET_URL = "https://ticket.melon.com/performance/index.htm?prodId=209991"

def send_slack_message(message):
    """Slack Webhook으로 메시지 전송"""
    payload = {"text": message}
    response = requests.post(SLACK_WEBHOOK_URL, json=payload)
    if response.status_code != 200:
        print("Slack 알림 실패:", response.text)

def check_ticket():
    """멜론티켓 페이지에서 예매 가능 여부 확인"""
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    res = requests.get(MELON_TICKET_URL, headers=headers)
    res.raise_for_status()

    soup = BeautifulSoup(res.text, "html.parser")

    # ✅ 예시: "예매가능" 또는 "취소표" 텍스트가 있는지 확인
    if "예매가능" in soup.text or "취소표" in soup.text:
        print("🎉 티켓이 열렸습니다!")
        send_slack_message("🎉 [멜론티켓] 취소표가 나왔습니다!\n👉 " + MELON_TICKET_URL)
    else:
        print("아직 티켓 없음.")

if __name__ == "__main__":
    check_ticket()
