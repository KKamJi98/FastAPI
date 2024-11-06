from fastapi import FastAPI, Header, Response

app = FastAPI()


# http localhost:8000/agent
@app.get("/agent")
def get_agent(user_agent: str = Header()):
    return user_agent


# http localhost:8000/header/input_name/input_value
@app.get("/header/{name}/{value}")
def header(name: str, value: str, response: Response):
    response.headers[name] = value
    return {"name": name, "value": value}
