FROM python:3.7.3-alpine3.9

WORKDIR /api

COPY requirements.txt .

RUN pip3 install -U pip && pip3 install -r requirements.txt

COPY api/ api/

ENTRYPOINT [ "python3", "-m", "api" ]