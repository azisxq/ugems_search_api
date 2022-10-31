FROM python:3.7.13

COPY * /app/

WORKDIR /app

RUN pip install -r requirements.txt

CMD ["python", "runserver.py"]

