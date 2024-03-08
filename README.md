# wikipedia counter

* flask app
* use wikipedia api to return number of views for an article for a given month


## docker

build:

```bash
docker build -t wikipedia-counter:latest .
```

build and run for dev:

```bash
docker run -p8181:8181 -it $(docker build -q .)
```


## examples of targets:

- http://localhost:8181/api/1/count?month=2020-12&article=G%C3%B6del%27s_incompleteness_theorems
- http://localhost:8181/api/1/count?month=2021-01&article=Python 
- http://localhost:8181/api/1/count?month=2015-10&article=Albert_Einstein


# install as python package

See `./wikipedia_counter/README.md`.
