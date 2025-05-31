from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def getData():
    return {"message": "Hello, World 2!"}