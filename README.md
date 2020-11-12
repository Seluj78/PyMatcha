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
 - [What does it look like](#what-does-it-look-like)
 - [How long did it take](#how-long-did-it-take)
 - [How many lines of code](#how-many-lines-of-code)
 - [What are the features](#features-implemented)
    - [What are the bonuses](#bonuses-implemented)

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

 - Backend on port `8080`
 - Frontend on port `4242`
 - Swagger doc on `9000`
 - PHPMyAdmin for debug on `8183`
 - Workers on internal port
 - Redis on `6379`
 - MySQL on internal port

### What does it look like
![Home page](https://github.com/seluj78/PyMatcha/blob/dev/screenshots/home_page.jpg?raw=true)
![Recommended profiles](https://github.com/seluj78/PyMatcha/blob/dev/screenshots/recommended_profiles.jpg?raw=true)
![Search page](https://github.com/seluj78/PyMatcha/blob/dev/screenshots/search_page.png?raw=true)
![Search no results](https://github.com/seluj78/PyMatcha/blob/dev/screenshots/search_no_results.png?raw=true)
![Search results](https://github.com/seluj78/PyMatcha/blob/dev/screenshots/search_results.jpg?raw=true)
![Profile settings](https://github.com/seluj78/PyMatcha/blob/dev/screenshots/profile_settings.png?raw=true)
![History](https://github.com/seluj78/PyMatcha/blob/dev/screenshots/history.jpg?raw=true)
![Profile](https://github.com/seluj78/PyMatcha/blob/dev/screenshots/unmatched_profile.png?raw=true)
![Matched profile](https://github.com/seluj78/PyMatcha/blob/dev/screenshots/matched_profile.jpg?raw=true)
![Matches and chat](https://github.com/seluj78/PyMatcha/blob/dev/screenshots/matches_chat.png?raw=true)

### How long did it take
Lauris and Jules started working on it at the begining of september and finished on `XXX`.
If you see commits before September, it's of an older version where Jules changed twice of frontend partner
Here is a nice visual representation of the commits:

gource

### How many lines of code
As of Thu 12 Nov 11:40
```
     637 text files.
     624 unique files.                                          
     164 files ignored.

github.com/AlDanial/cloc v 1.88  T=1.68 s (333.3 files/s, 17377.3 lines/s)
-------------------------------------------------------------------------------
Language                     files          blank        comment           code
-------------------------------------------------------------------------------
JSON                           329              0              0           7924
Python                         119           1560           2126           5633
Vuejs Component                 53            146             91           4492
YAML                             7             32             22           2531
XML                             14              0              0           2042
JavaScript                      21             44             35           1156
CSS                              5             61              5            459
HTML                             4              0             22            253
SQL                              1             43             66            202
Markdown                         4             42              0            139
TOML                             1              3              5             21
Dockerfile                       1             12              0             18
SVG                              1              0              0              8
-------------------------------------------------------------------------------
SUM:                           560           1943           2372          24878
-------------------------------------------------------------------------------
```

### Features implemented
 - Sign-up and sign-in
    - Forgot password email
    - Resend confirmation email
    - Registration process to add info on user
 - Browse recommended users
    - Filter them
    - Sort them
 - Search users
    - Filter them
    - Sort them
 - Like and superlike a user
 - Notifications for:
    - Like
    - Unlike
    - Match
    - Message
  - Chat with instant replies
  - Settings page where you can modify everything
  - History page 

#### Bonuses implemented
 - Superlikes
 - [CI/CD](https://github.com/Seluj78/PyMatcha/blob/dev/.travis.yml)
 - [Postman API tests](https://github.com/Seluj78/PyMatcha/blob/dev/PyMatchaV2.postman_collection.json)
 - Bots
 - [Swagger API Documentation](https://github.com/Seluj78/PyMatcha/blob/dev/backend/schemas/swagger.yaml)
