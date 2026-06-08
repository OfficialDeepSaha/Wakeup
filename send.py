import time
import requests
from datetime import datetime

urls = ["https://api.prepsathi.co.in/health", "https://api.prepsathi.co.in/"]

print("Keep-awake script started...")
while True:

    for url in urls:
        try:

            response = requests.get(url, timeout=5)
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Ping status: {response.status_code}") # Line truncated in screenshot, assumed .status_code
        except requests.exceptions.RequestException as e:
            pass # Exception block collapsed in screenshot

    time.sleep(20) # Pause for 30 seconds
