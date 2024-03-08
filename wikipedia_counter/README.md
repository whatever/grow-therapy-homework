# wikipedia counter

* flask app
* use wikipedia api to return number of views for an article for a given month


## examples of targets:

- http://localhost:8181//api/1/count?month=2020-12&article=G%C3%B6del%27s_incompleteness_theorems
- http://localhost:8181/api/1/count?month=2021-01&article=Python 
- http://localhost:8181/api/1/count?month=2015-10&article=Albert_Einstein


# install package

```bash
pip3 install -e .
pip3 install -e ".[dev]"
```
