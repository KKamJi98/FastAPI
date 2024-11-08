import uvicorn
from fastapi import FastAPI
from app.web import explorer, creature


app = FastAPI()

app.include_router(explorer.router)
app.include_router(creature.router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True)
