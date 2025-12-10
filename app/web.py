from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "LinkedIn Auto Post backend online"}
