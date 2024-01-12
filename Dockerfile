FROM python
MAINTAINER ayerman

RUN python -m ensurepip --upgrade

COPY . .

ARG WATTSY_VERSION
ENV WATTSY_VERSION=$WATTSY_VERSION
LABEL version=$WATTSY_VERSION

RUN python -m pip install -r requirements.txt

CMD [ "python", "main.py" ]

# docker build --build-arg WATTSY_VERSION=${CI_COMMIT} -t discord-bot .