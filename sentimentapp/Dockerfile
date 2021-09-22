FROM python:3.8-slim-buster

COPY requirements.txt /

RUN pip3 install -r /requirements.txt

COPY sentimentapp/ /app
WORKDIR /app

EXPOSE 5000

ENTRYPOINT ["gunicorn", "app:app", "--threads", "5", "-b", "0.0.0.0:5000"]
