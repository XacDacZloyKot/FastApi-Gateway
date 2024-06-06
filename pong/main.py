from fastapi import FastAPI, Body
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/process")
def process_endpoint(data=Body()):
    print(f"Processing data: {data} | Время {datetime.now()}")
    # return {"message": "Data processed", "data": data}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)