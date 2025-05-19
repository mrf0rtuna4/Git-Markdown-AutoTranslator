FROM python:3.9.16-slim AS builder

RUN useradd --create-home appuser
WORKDIR /home/appuser
USER appuser

COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

COPY core ./core

ENTRYPOINT ["python", "core/main.py"]