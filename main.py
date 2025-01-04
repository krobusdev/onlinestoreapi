from fastapi import FastAPI
from adapters.api import router

app = FastAPI()
app.include_router(router)