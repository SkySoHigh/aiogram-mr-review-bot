FROM python:3.8-slim

ENV WORK_DIR /review-bot

COPY ./  $WORK_DIR/

WORKDIR $WORK_DIR

RUN set +x \
 && apt update \
 && apt upgrade -y \
 && pip3 install -r requirements.txt

CMD ["python3", "run.py"]
