FROM python:3.11

ENV HOST=0.0.0.0
ENV PORT=8181
ENV WORKERS=2

RUN pip3 install --upgrade pip

WORKDIR /wikipedia-counter

COPY wikipedia_counter .

RUN echo 1
RUN pip3 install "."

CMD wikipedia-counter --workers $WORKERS --host $HOST --port $PORT
