FROM python:3.8 as builder

WORKDIR /app

COPY requirements.txt ./

COPY core core

RUN pip install -r requirements.txt

RUN yarn build:action

FROM python:3.8
WORKDIR /action-end

COPY --from=builder /app/core/dist/ /action-end/

CMD ["python", "core/translator"]
