FROM python:3.12-alpine

# Don't generate .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
# Force unbuffered output
ENV PYTHONUNBUFFERED=1

LABEL app_name="Popcat Url Shortener"
LABEL description="Popcat Url Shortener is a Public Version of the Original Shortener"
LABEL version="1.0.0"
LABEL maintainer="Herr Erde"

WORKDIR /app

COPY src/ .

RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "main.py"]
