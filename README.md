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

## Running the server

|        Key       | Value                           | Comment                                                                                   |
|:----------------:|---------------------------------|-------------------------------------------------------------------------------------------|
| FLASK_ENV        | Either `prod` or `dev`          | If this variable is set to `dev`, then no need to supply FLASK_DEBUG and FLASK_SECRET_KEY |
| FLASK_DEBUG      | True or False                   |                                                                                           |
| FLASK_SECRET_KEY | A secret key to encrypt cookies |                                                                                           |

```bash
python app.py
```
