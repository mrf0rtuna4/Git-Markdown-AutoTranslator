FROM python:3.8

WORKDIR /core

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY core/app /core/app

ENTRYPOINT ["python", "/core/app/main.py"]
