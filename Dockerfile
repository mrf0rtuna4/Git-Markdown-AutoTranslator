FROM python:3.8

WORKDIR /core

COPY requirements.txt /core/

RUN pip install -r /core/requirements.txt

COPY core /core/core

ENTRYPOINT ["python", "/core/core/app/main.py"]
