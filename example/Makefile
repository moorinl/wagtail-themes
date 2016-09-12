all: clean install migrate loaddata runserver

clean:
	find . -name '*.pyc' | xargs rm

install:
	pip install -r requirements.txt

migrate:
	python manage.py migrate

loaddata:
	python manage.py loaddata fixtures/users.json
	python manage.py loaddata fixtures/pages.json
	python manage.py loaddata fixtures/sites.json
	python manage.py loaddata fixtures/themes.json

runserver:
	python manage.py runserver
