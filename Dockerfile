FROM python:3.10-slim

RUN apt-get update && apt-get install -y default-jdk wget curl gnupg2 apt-transport-https && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

RUN pip install --no-cache-dir pyspark

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "sentiment_server.py"]
