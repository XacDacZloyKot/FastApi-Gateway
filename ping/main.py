from fastapi import FastAPI
import requests
import random

app = FastAPI()


def generate_unique_requests(n):
    unique_requests = [f'unique_request_{i}' for i in range(n)]
    return unique_requests


def send_requests():
    url = 'http://localhost:8000/gateway/'
    unique_requests = generate_unique_requests(400)
    repeat_requests = [random.choice(unique_requests) for _ in range(random.randint(300, 400))]
    all_requests = unique_requests + repeat_requests

    for request_data in all_requests:
        try:
            request_dict = {'data': request_data}
            print(request_dict)
            response = requests.post(url, data=request_dict)
            print(response.text)
        except Exception as e:
            print(f"Error: {e}")


@app.post("/send_requests")
async def start_send_requests():
    send_requests()
    return {"message": "Requests sending has completed."}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
