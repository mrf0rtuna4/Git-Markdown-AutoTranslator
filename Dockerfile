FROM python:3.8

WORKDIR /app

COPY requirements.txt ./

COPY core core

RUN pip install -r requirements.txt

CMD ["python", "/core/translator"]