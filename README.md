# wikipedia counter

Back-end web application that acts as a wrapper around the Wikipedia API:

* flask app
* use wikipedia api to return number of views for an article for a given month


## docker

build:

```bash
# Via Dockerfile
docker build -t wikipedia-counter:latest .

# Or via Makefile:
make build
```

build and run for dev:

```bash
# docker
docker run -p8181:8181 -it $(docker build -q .)

# make
make run
```

test:

```bash
make test
```

## examples of targets:

- http://localhost:8181/api/1/count?month=2020-12&article=G%C3%B6del%27s_incompleteness_theorems
- http://localhost:8181/api/1/count?month=2021-01&article=Python 
- http://localhost:8181/api/1/count?month=2015-10&article=Albert_Einstein

## example response:

```bash
curl -s "http://localhost:8181/api/1/count?month=2021-01&article=Python" | jq .
{
  "count": 14423,
  "status": "ok"
}
```


# install as python package

See `./wikipedia_counter/README.md`.
