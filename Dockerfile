FROM python:3.9-slim-buster 


RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN python3.9 -m pip install --upgrade pip==21.2.4

WORKDIR /demo/


COPY . /demo/

RUN pip install -r req.txt

EXPOSE 5000

ENTRYPOINT ["python3.9"]
CMD ["app.py"]

