import time
import asyncio
from contextlib import asynccontextmanager
import requests
from datetime import datetime
from fastapi import FastAPI
import uvicorn

# 1. Your list of URLs (including the new Render URL)
urls = [
    "https://api.prepsathi.co.in/health", 
    "https://api.prepsathi.co.in/",
    "https://wakeup-g5sp.onrender.com/"
]

# 2. Background task for the keep-awake loop
async def keep_awake_loop():
    print("Keep-awake background script started...")
    while True:
        for url in urls:
            try:
                # Running requests.get in an executor prevents blocking the async loop
                loop = asyncio.get_event_loop()
                response = await loop.run_in_executor(None, lambda: requests.get(url, timeout=5))
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Pinged {url} | Status: {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Failed to ping {url}: {e}")
        
        await asyncio.sleep(20)  # Pause for 20 seconds asynchronously

# 3. Lifespan manager to start the background task on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start the background loop
    asyncio.create_task(keep_awake_loop())
    yield
    # Clean up actions can go here if needed

# 4. Initialize FastAPI app
app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"status": "alive", "message": "Keep-awake service is running."}

# 5. Uvicorn configuration to specify port 8000
if __name__ == "__main__":
    uvicorn.run("send.py:app", host="0.0.0.0", port=8000, reload=False)
