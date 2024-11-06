from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()


@app.get("/happy")
def happy():
    return JSONResponse(status_code=590, content={"message": "Happy"})
