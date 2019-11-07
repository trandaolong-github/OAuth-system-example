FROM python:3.7-alpine

EXPOSE 5001

WORKDIR /System_test

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD py.test --color=yes --verbose --junit-xml=junit-xml-result.xml test_oauth_system.py