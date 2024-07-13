FROM python:3.8

WORKDIR /project

# 👇
COPY requirements.txt ./
RUN pip install -r requirements.txt
# 👆

COPY . .

ENTRYPOINT ["python", "/core/main.py"]
