# PyMatcha
Python Matcha Dating Website

## Installation

Create a virtual environnement

```bash
python3 -m venv venv
```

Activate the virtual environnement

```bash
source venv/bin/activate
```

Install the requirements

```bash
pip install -r requirements.txt
```

## Dev install

Install pre-commit

```bash
pip install pre-commit
pre-commit install
```

## Running the server

|        Key       | Value                             | Comment                                                                                                                                                 |
|:----------------:|-----------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------|
| FLASK_ENV        | Either `prod` or `dev`            | If this variable is set to `dev`, then no need to supply FLASK_DEBUG and FLASK_SECRET_KEY                                                               |
| FLASK_DEBUG      | True or False                     |                                                                                                                                                         |
| FLASK_SECRET_KEY | A secret key to encrypt cookies   |                                                                                                                                                         |
| DB_USER          | Database user                     |                                                                                                                                                         |
| DB_PASSWORD      | Database password                 |                                                                                                                                                         |
| DB_HOST          | Database host                     | must be `pymatchadb.cvesmjtn6kz7.eu-west-3.rds.amazonaws.com`  for production or `pymatchadb-tests.cvesmjtn6kz7.eu-west-3.rds.amazonaws.com`  for tests |
| CI               | Is the server in a CI environment |  Must be set to 0 if on a prod environement. If set to 1, will erase the test DB.                                                                       |

```bash
python app.py
```


## Running tests

### Flake8

```bash
flake8
```

```bash
export FLASK_DEBUG=1 && export FLASK_SECRET_KEY=ThisIsADevelopmentKey && export DB_USER=pymatcharoot && export DB_PASSWORD=PASSWORD && export DB_HOST='pymatchadb-tests.cvesmjtn6kz7.eu-west-3.rds.amazonaws.com' && export CI=1 && python -m pytest
```