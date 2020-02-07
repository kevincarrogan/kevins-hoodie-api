import httpx
import json

from datetime import date
from typing import List

from fastapi import FastAPI
from pydantic import BaseModel
from pydantic.color import Color

app = FastAPI()


class Day(BaseModel):
    colour: str = None
    hex: Color = None
    date: date


class Days(BaseModel):
    days: List[Day]


@app.get("/days/", response_model=Days)
async def days():
    colours_url = "https://raw.githubusercontent.com/kevincarrogan/whatcolourhoodieiskevinwearingtoday.com/master/data/colours.json"

    async with httpx.AsyncClient() as client:
        response = await client.get(colours_url)

    return {"days": response.json()}


@app.post("/days/", response_model=Day)
def add_day(day: Day):
    return day
