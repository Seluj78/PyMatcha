![GitHub](https://img.shields.io/github/license/seluj78/pymatcha?style=for-the-badge) ![Travis (.com)](https://img.shields.io/travis/com/seluj78/pymatcha/dev?label=builds%20and%20tests&style=for-the-badge) ![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/seluj78/pymatcha?style=for-the-badge) ![Libraries.io dependency status for GitHub repo](https://img.shields.io/librariesio/github/seluj78/pymatcha?style=for-the-badge)
# PyMatcha
#### Made by [Jules Lasne](https://github.com/seluj78) and [Lauris Skrauci](https://github.com/suppalarry) 

## Summary
 - [Why ?](#why)
 - [Installation](#installation)
   - [For Production](#for-production)
   - [For developpment](#for-developpment)
      - [Backend](#backend)
      - [Workers](#workers)
      - [Frontend](#frontend)
 - [Services in docker-compose](#the-different-services-on-the-docker-compose)
 - [What does it look like]([what-does-it-look-like)
 - [How long did it take](how-long-did-it-take)
 - [How many lines of code](how-many-lines-of-code)
 - [What are the features](what-are-the-features)
 - [What are the bonuses](any-bonuses)

### Why ?
Matcha is a [42](https://42.fr) school project aiming to teach how to make a dating website. Lauris and Jules chose to make it as close as it could be to a real production product.
You can find the subject [here](https://github.com/Seluj78/PyMatcha/blob/dev/subject.pdf)

### Installation
#### For production
You can simply download or git clone the project and, once inside of it, run `docker-compose up --build`.
The website will be accessible on port `4242`.
#### For developpment
First of all, clone or download the repository, extract it if necessary then cd into it.

##### Backend:
You'll need `python3.8`+. cd in the backend and run:
```shell
python3.8 -m venv venv --prompt PyMatcha
```
```shell
source venv/bin/activate
```
```shell
pip install backend/requirements.txt
```
```shell
python run.py
```

##### Workers:
Same thing as for the backend, just then `cd` in the backend folder and run
```shell
celery -A PyMatcha.celery worker -E --loglevel=INFO -B --pool=threads
```

##### Frontend:
`cd` in the frontend folder and run `yarn install` then `yarn run`

### The different services on the docker-compose:

### What does it look like?
Screenshots here

### How long did it take?
Lauris and Jules started working on it at the begining of september and finished on `XXX`.
If you see commits before September, it's of an older version where Jules changed twice of frontend partner
Here is a nice visual representation of the commits:

gource

### How many lines of code?
cloc

### What are the features ?
 - Feature list

### Any bonuses ?
 - Bonuses list
