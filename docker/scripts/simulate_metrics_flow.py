import asyncio
import aiohttp
import time
from jose import jwt

# === Configuration ===
BASE_URL = "http://app:8000"
USER_ID = "1"
SECRET_KEY = "mysecret"
ALGORITHM = "HS256"
REQUESTS = 15
CONCURRENCY = 5

# === Generate a valid JWT token ===
def generate_valid_token(user_id: str) -> str:
    payload = {
        "sub": user_id,
        "exp": 9999999999  # optional: large future expiration
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return f"Bearer {token}"

# === Wait until the API is ready ===
async def wait_for_api(max_retries=10):
    print("[...] Waiting for the API to become available...")
    for attempt in range(1, max_retries + 1):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{BASE_URL}/docs") as resp:
                    if resp.status == 200:
                        print("[✓] API is ready to receive requests.\n")
                        return
        except Exception:
            pass
        print(f"[!] Attempt {attempt}/{max_retries} failed. Retrying in 2s...")
        await asyncio.sleep(2)
    raise Exception("API did not respond after multiple attempts.")

# === Simulate a single API request ===
async def fetch_metrics(session, i, token):
    headers = {"Authorization": token}
    url = f"{BASE_URL}/users/{USER_ID}/metrics"
    start = time.perf_counter()

    try:
        async with session.get(url, headers=headers) as response:
            duration = time.perf_counter() - start
            status = response.status
            if status == 200:
                data = await response.json()
                print(f"[✓] Req {i} OK ({duration:.2f}s):", data.get("summary", data))
            elif status == 429:
                print(f"[!] Req {i} BLOCKED: Rate Limit")
            else:
                print(f"[x] Req {i} ERROR ({status}):", await response.text())
    except Exception as e:
        print(f"[x] Req {i} FAILED:", e)

# === Run the full load test ===
async def run_load_test():
    await wait_for_api()
    token = generate_valid_token(USER_ID)

    connector = aiohttp.TCPConnector(limit=None)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = []
        for i in range(REQUESTS):
            tasks.append(fetch_metrics(session, i + 1, token))
            if (i + 1) % CONCURRENCY == 0:
                await asyncio.gather(*tasks)
                tasks = []
                await asyncio.sleep(2)
        if tasks:
            await asyncio.gather(*tasks)

# === Script entry point ===
if __name__ == "__main__":
    asyncio.run(run_load_test())
