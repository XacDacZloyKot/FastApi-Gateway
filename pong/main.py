from fastapi import FastAPI, Request


app = FastAPI()


@app.post("/process")
async def process_endpoint(request: Request):
    data = await request.json()
    print(f"Processing data: {data}")
    return {"message": "Data processed", "data": data}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)