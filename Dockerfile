FROM python:3.9.16-slim AS builder

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY core ./core

ENTRYPOINT ["python", "core/main.py"]