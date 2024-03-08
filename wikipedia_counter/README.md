# wikipedia_counter

Back-end web application that acts as a wrapper around the Wikipedia API.

## Install

```bash
pip3 install -e ".[dev]"
```

## CLI

```bash
wikipedia-counter --host 0.0.0.0 --port 8181 --workers 2
```


## Test

```bash
pip3 install -e ".[dev]"
pytest
flake8
```
