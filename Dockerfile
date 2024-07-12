FROM python:3.8

COPY requirements.txt /requirements.txt

COPY core /core

COPY core/app /core/app

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "/core/main.py"]
