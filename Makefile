.PHONY: build run test

build:
	docker build -t wikipedia-counter:latest .

run:
	docker run -p8181:8181 -it $(shell docker build -q .)

test:
	docker run -it $(shell docker build -q .) pytest
