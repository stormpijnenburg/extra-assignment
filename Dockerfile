FROM python:3.10-alpine

# Install system dependencies needed for mysqlclient
RUN apk update && apk add mariadb-dev gcc musl-dev

WORKDIR /app

COPY requirements.txt requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD [ "python3", "app.py"]

