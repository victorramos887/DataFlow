from fastapi import FastAPI

app = FastAPI(title="PipelinesOps API")

@app.get("/")
async def read_root():
    return {"message": "Welcome to the PipelinesOps API!"}