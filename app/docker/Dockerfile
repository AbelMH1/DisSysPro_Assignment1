# FROM python:3.8-slim-buster
FROM python:3-stretch

WORKDIR /app

COPY . /app
# RUN pip install --trusted-host pyip.python.org tinydb
RUN pip install --trusted-host pyip.python.org -r requirements.txt

# EXPOSE 50053
EXPOSE 50051

CMD [ "python", "player_statsV2.py" ]