FROM python:3.8 as builder

WORKDIR /app

COPY requirements.txt ./

COPY core core

RUN export YARN_CACHE_FOLDER="$(mktemp -d)"
RUN pip install -r requirements.txt

RUN yarn build

FROM python:3.8
WORKDIR /action-end

RUN export YARN_CACHE_FOLDER="$(mktemp -d)"
COPY --from=builder /app/core/ /action-end/

CMD ["python", "/core/translator"]