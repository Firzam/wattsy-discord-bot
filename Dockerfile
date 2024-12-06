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

COPY src/* /app

COPY source-env.sh .
RUN chmod +x source-env.sh

CMD [ "source-env.sh" ]

# docker build --build-arg WATTSY_VERSION=${CI_COMMIT} -t discord-bot .