FROM python:3.11-alpine

ENV PIP_ROOT_USER_ACTION=ignore
ENV HOST=0.0.0.0
ENV PORT=8181
ENV WORKERS=2

RUN pip3 install --upgrade pip

WORKDIR /wikipedia-counter

COPY wikipedia_counter .

RUN pip3 install "."

CMD wikipedia-counter --workers $WORKERS --host $HOST --port $PORT
