FROM python:3.9.20

ARG WATTSY_VERSION
ENV WATTSY_VERSION=$WATTSY_VERSION

LABEL maintainer=ayerman
LABEL version=$WATTSY_VERSION

RUN python -m ensurepip --upgrade

RUN apt-get update -y && apt-get upgrade -y
RUN apt-get install -y ffmpeg

COPY requirements.txt .

RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY src/* /app

CMD [ "python", "/app/main.py" ]

# docker build --build-arg WATTSY_VERSION=${CI_COMMIT} -t discord-bot .