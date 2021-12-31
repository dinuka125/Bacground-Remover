From python:3.9.7-slim

WORKDIR /app

ADD . /app

RUN pip install -r requirements.txt

CMD ["python", "app.py"]