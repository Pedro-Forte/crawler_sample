FROM python:3.8.10

COPY . /app

WORKDIR /app

RUN pip3 install -r requirements.txt

CMD ["python3", "./cialdnb/runner.py"]