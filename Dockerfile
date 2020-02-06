FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7-alpine3.8

COPY ./requirements-prod.txt ./requirements-prod.txt

RUN pip install -r requirements-prod.txt

COPY ./app /app
