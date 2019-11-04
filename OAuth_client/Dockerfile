FROM python:3.7-alpine

EXPOSE 5000

WORKDIR /OAuth_client

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3", "app.py"]