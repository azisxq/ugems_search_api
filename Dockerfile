FROM python:3.7.13

COPY * /app/

WORKDIR /app

RUN pip install --proxy http://10.12.51.11:3128 -r requirements.txt

CMD ["python", "runserver.py"]

