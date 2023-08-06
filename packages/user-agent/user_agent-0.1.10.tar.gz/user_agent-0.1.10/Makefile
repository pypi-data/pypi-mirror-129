.PHONY: clean release build venv deps viewdoc

clean:
	find -name '*.pyc' -delete
	find -name '*.swp' -delete
	find -name __pycache__ -delete

build: venv deps

venv:
	virtualenv --no-site-packages --python=python3 .env

deps:
	.env/bin/pip install -r requirements_dev.txt

viewdoc:
	x-www-browser docs/build/html/index.html

release:
	git push; git push --tags; rm dist/*; python3 setup.py clean sdist; twine upload dist/*
