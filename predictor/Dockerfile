FROM python:3.9.7

RUN apt-get update
RUN apt-get install -y cmake
RUN pip install --upgrade pip

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
EXPOSE 7000

CMD ["uvicorn", "predictor:app","--host", "0.0.0.0", "--port", "7000"]