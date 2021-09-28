FROM python:3.8-slim-buster

COPY requirements.txt /

RUN pip3 install -r /requirements.txt && python -m textblob.download_corpora

WORKDIR /app
ADD . .

ENTRYPOINT ["python", "webnlp.py"]
