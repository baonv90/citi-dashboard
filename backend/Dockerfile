FROM python:3.8-slim-buster
WORKDIR /app
COPY ./src /app/backend
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
CMD uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload