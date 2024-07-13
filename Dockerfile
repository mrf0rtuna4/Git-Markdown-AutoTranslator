FROM python:3.8
COPY requirements.txt /requirements.txt

RUN pip install -r requirements.txt

COPY core /core

WORKDIR /core

COPY app /app

ENTRYPOINT ["python", "main.py"]
