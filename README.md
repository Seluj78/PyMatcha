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

## Temporary TODO List (Will be moved to issues)

- Logging
- Flake8
- Mypy
- nosetests/pytests
- Pre commit hooks
- Travis
- EC2
- API Doc
- Issues with commits
- PR workflow (suggestions, request reviews)
- Projects github
- Milestone github
- Folders for flask (see https://github.com/Seluj78/juleslasne/tree/master/website)
- Explain license and encoding header
- Explain how imports are organized
- Explain flake8 + mypy
- Explain commit lenght is important. verbose FTW
