FROM python:3.8

COPY requirements.txt /requirements.txt

COPY core /core

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "/core/main.py"]
