import asyncio
from contextlib import asynccontextmanager
import os
import requests
from datetime import datetime
from fastapi import FastAPI
import uvicorn

# GET URLs to ping
urls = [
    "https://api.prepsathi.co.in/health",
    "https://api.prepsathi.co.in/",
    "https://wakeup-g5sp.onrender.com/",
    "https://prepsathi-backend.onrender.com/",
]

# POST login requests to send
post_requests = [
    {
        "url": "https://api.prepsathi.co.in/auth/login",
        "payload": {
            "email": "deepsaha01896@gmail.com",
            "password": "deePs223@#"
        }
    }
]

async def keep_awake_loop():
    print("Keep-awake background script started...")

    while True:
        # Send GET requests
        for url in urls:
            try:
                loop = asyncio.get_running_loop()
                response = await loop.run_in_executor(
                    None,
                    lambda u=url: requests.get(u, timeout=5)
                )
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Pinged {url} | Status: {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Failed to ping {url}: {e}")

        # Send POST login request(s)
        for req in post_requests:
            try:
                loop = asyncio.get_running_loop()
                response = await loop.run_in_executor(
                    None,
                    lambda r=req: requests.post(r["url"], json=r["payload"], timeout=10)
                )
                print(f"[{datetime.now().strftime('%H:%M:%S')}] POSTed {req['url']} | Status: {response.status_code}")
                print(f"Response: {response.text}")
            except requests.exceptions.RequestException as e:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Failed to POST {req['url']}: {e}")

        await asyncio.sleep(15)

@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(keep_awake_loop())
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"status": "alive", "message": "Keep-awake service is running."}

if __name__ == "__main__":
    uvicorn.run("send:app", host="0.0.0.0", port=8000, reload=False)
