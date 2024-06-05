from fastapi import FastAPI, Request
from redis import Redis

from hashlib import sha256
import json

from tasks import send_request

app = FastAPI()
redis = Redis(host="localhost", port=6379, db=0)


def hash_request(data):
    return sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()


@app.post("/gateway")
async def gateway(request: Request):
    data = await request.json()
    request_hash = hash_request(data)

    if redis.get(request_hash):
        return {"status": "duplicate request"}

    # Кеш ???
    await redis.set(name=request_hash, value=1, ex=300)

    # Отправка запроса в очередь
    send_request.apply_async(queue='message', kwargs={'data': data})
    return {"status": "request accepted"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)