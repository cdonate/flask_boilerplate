FROM python:3.5

ARG PORT
ENV PORT_ENV ${PORT}

ARG GUNICORN_WORKERS
ENV GUNICORN_WORKERS_ENV ${GUNICORN_WORKERS}


ADD . /python-flask-api
WORKDIR /python-flask-api

# This is for you use the POSTGRES with SQLAlchemy
RUN apt-get update -y
RUN apt-get install postgresql -y
RUN apt-get install python-psycopg2 -y
RUN apt-get install libpq-dev -y
RUN apt-get install python3-dev -y

RUN pip install -r requirements.txt
RUN export $(cat .env | xargs)

EXPOSE $PORT

CMD gunicorn -w ${GUNICORN_WORKERS} -b 0.0.0.0:${PORT_ENV} app.initialize:web_app