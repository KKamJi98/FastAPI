import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI()

secret_user: str = "newphone"
secret_password: str = "whodis?"

basic: HTTPBasicCredentials = HTTPBasic()


@app.get("/who")
def get_user(credentials: HTTPBasicCredentials = Depends(basic)) -> dict:
    if credentials.username == secret_user and credentials.password == secret_password:
        return {"username": credentials.username, "password": credentials.password}
    raise HTTPException(status_code=401, detail="Incorrect username or password")


if __name__ == "__main__":
    uvicorn.run("auth:app", reload=True)
