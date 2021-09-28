FROM python:3.8-slim-buster

COPY requirements.txt /

RUN pip3 install -r /requirements.txt

ENV NLTK_DATA=/app
RUN python -m textblob.download_corpora

COPY sentimentapi/ /app
WORKDIR /app

EXPOSE 8000

ENTRYPOINT ["gunicorn", "api:app", "--threads", "5", "-b", "0.0.0.0:8000"]
