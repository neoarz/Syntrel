FROM python:3.12.9-slim-bookworm

WORKDIR /bot
COPY . /bot

RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

RUN python -m pip install -r requirements.txt

ENTRYPOINT [ "python", "bot.py" ]