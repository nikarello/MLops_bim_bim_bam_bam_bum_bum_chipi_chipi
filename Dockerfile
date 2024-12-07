FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt /app/

RUN apt-get update && apt-get install -y git wget && apt-get clean
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

CMD ["python", "app/main.py"]
