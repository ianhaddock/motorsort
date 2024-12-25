# Pytest tests

### Setup
* setup a python venv
* pip install -r requirements.txt
* from project root run the following to generate a report:

```
$ pytest -vv -x --cov-report term-missing --cov=app tests
```

### Notes
* Last two tests in test_motorsort.py are not unit tests and should be revisited.
