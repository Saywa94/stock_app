FROM python:3.6-alpine

RUN adduser -D stock-app

WORKDIR /home/stock-app

COPY requirements.txt requirements.txt

RUN python -m venv .venv
RUN .venv/bin/pip install -r requirements.txt

COPY stockapp stockapp
COPY migrations migrations
COPY run.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP run.py

RUN chown -R stock-app:stock-app ./
USER stock-app

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
