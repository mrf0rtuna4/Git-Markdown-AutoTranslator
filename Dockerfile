FROM python:3.8
COPY requirements.txt /requirements.txt

RUN pip install -r requirements.txt

COPY core ./core

COPY ./core/app/*.py ./core/app/

ENTRYPOINT ["python", "main.py"]
