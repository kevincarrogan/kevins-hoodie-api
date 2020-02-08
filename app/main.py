import boto3
import httpx
import json
import os

from datetime import date
from typing import List

from fastapi import FastAPI, HTTPException, Security
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from pydantic.color import Color
from starlette.status import HTTP_403_FORBIDDEN

app = FastAPI()


class Hex(Color):
    def __str__(self):
        return self.original()


class Day(BaseModel):
    colour: str = None
    hex: Hex = None
    date: date


class Days(BaseModel):
    days: List[Day]


api_key_header = APIKeyHeader(name="api-key")
api_key = os.environ["API_KEY"]


@app.get("/days/", response_model=Days)
async def days(*, api_header: str = Security(api_key_header)):
    if api_header != api_key:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Not authenticated")
    colours_url = "https://raw.githubusercontent.com/kevincarrogan/whatcolourhoodieiskevinwearingtoday.com/master/data/colours.json"

    async with httpx.AsyncClient() as client:
        response = await client.get(colours_url)

    return {"days": response.json()}


@app.post("/days/")
def add_day(day: Day):
    return day


dynamodb = boto3.resource("dynamodb", region_name="eu-west-2")


table = dynamodb.Table("colours")


@app.get("/colours/")
def colours():
    return {"colours": table.scan()["Items"]}
