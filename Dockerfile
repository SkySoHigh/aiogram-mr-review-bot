FROM python:3.8-slim

ENV WORK_DIR /review-bot

COPY ./  $WORK_DIR/

WORKDIR $WORK_DIR

RUN set +x \
 && apt update \
 && apt upgrade -y \
 && apt install -yq tzdata \
 && ln -fs /usr/share/zoneinfo/Europe/Moscow /etc/localtime \
 && dpkg-reconfigure -f noninteractive tzdata \
 && pip3 install -r requirements.txt

VOLUME data
VOLUME logs
VOLUME configs

CMD exec python3 run.py >> ./logs/out.log 2>&1
