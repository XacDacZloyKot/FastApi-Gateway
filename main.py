import asyncio
from fastapi import FastAPI, BackgroundTasks
import aiohttp
import random

app = FastAPI()


async def send_requests():
    url = 'http://localhost:8000/gateway'  # Используем локальный адрес
    async with aiohttp.ClientSession() as session:
        tasks = []
        for _ in range(random.randint(300, 900)):  # Отправляем случайное количество запросов
            tasks.append(send_request(session, url))
        await asyncio.gather(*tasks)


async def send_request(session, url):
    try:
        # Отправляем POST запрос на эндпоинт /gateway
        async with session.post(url, data={'key': 'value'}) as response:
            return await response.text()  # Возвращаем ответ сервера
    except Exception as e:
        return f"Error: {e}"


@app.post("/send_requests")
async def start_send_requests(background_tasks: BackgroundTasks):
    background_tasks.add_task(send_requests)
    return {"message": "Requests sending has started."}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
