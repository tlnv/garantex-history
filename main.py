from fastapi import FastAPI
from pydantic import BaseModel


import parsing


app = FastAPI()


@app.get("/otc/")
async def get_otc():
    return parsing.observe()