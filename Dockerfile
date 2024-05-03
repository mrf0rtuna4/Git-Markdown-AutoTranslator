FROM python:3.8

WORKDIR /app

COPY requirements.txt ./

COPY core core

RUN pip install -r requirements.txt

COPY --from=builder /app/core/dist/ dist/

CMD ["python", "/app/core/translator.py"]
