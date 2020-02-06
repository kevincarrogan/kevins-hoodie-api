import httpx
import json

from fastapi import FastAPI

app = FastAPI()


@app.get("/days/")
async def days():
    colours_url = "https://raw.githubusercontent.com/kevincarrogan/whatcolourhoodieiskevinwearingtoday.com/master/data/colours.json"

    async with httpx.AsyncClient() as client:
        response = await client.get(colours_url)

    return {"days": response.json()}
