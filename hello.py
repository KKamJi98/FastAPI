from fastapi import Response, FastAPI

app = FastAPI()


# @app.get("/hi/{who}")
# def greet(who):
#     return f"Hello? {who}?"

# Query Parameter
# @app.get("/hi")
# def greet(who):
#     return f"Hello? {who}?"

# POST Method
# @app.post("/hi")
# def greet(who: str = Body(embed=True)):
#     return f"Hello {who}"

# Header
# @app.get("/hi")
# def greet(who: str = Header()):
#     return f"Hello? {who}?"

# @app.get("/agent")
# def get_agent(user_agent: str = Header()):
#     return user_agent

# @app.get("/happy")
# def happy(status_code=400):
#     return ":)"


@app.get("/header/{name}/{value}")
def header(name: str, value: str, response: Response):
    response.headers[name] = value
    return "normal body"


# uvicorn hello:app --reload
# 8000번 포트
