FROM python:3.7.13

RUN mkdir -p /app/Modules

RUN mkdir -p /app/Modules/common

COPY runserver.py /app/

COPY requirements.txt /app/

COPY Modules/* /app/Modules/

COPY Modules/common/* /app/Modules/common

WORKDIR /app

RUN pip install --proxy http://10.12.51.11:3128 -r requirements.txt

CMD ["python", "runserver.py"]

