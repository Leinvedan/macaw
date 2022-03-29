setup:
	pip install -r requirements.txt

test:
	python -m unittest tests/*.py

lint:
	pylint macaw

run:
	python -m macaw

# == Docker ==
docker-build:
	docker build -t macaw-crawler .

docker-run:
	docker run \
		-ti \
		-v `pwd`:/usr/src/app \
		--env PYTHONPATH=/usr/src/app \
		macaw-crawler