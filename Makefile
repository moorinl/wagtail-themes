all: clean install

clean:
	find . -name '*.pyc' | xargs rm

install:
	pip install -e .
