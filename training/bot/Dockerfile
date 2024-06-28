FROM python:3.11-alpine3.20
COPY ./req.txt ./req.txt
RUN pip install --upgrade pip && pip install -r req.txt

WORKDIR /app
COPY ./main.py ./bot.py
COPY ./clean.py ./clean.py

ENTRYPOINT ["python", "./bot.py"]