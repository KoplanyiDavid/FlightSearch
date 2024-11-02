import requests
from constants import BOT_TOKEN, CHAT_ID

def send_message(message):
  url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage?chat_id={CHAT_ID}&text={message}"
  res = requests.get(url)
  if res.status_code == 200:
    return True
  else:
    return False