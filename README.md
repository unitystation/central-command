# Central Command

![Docker Image Version (latest by date)](https://img.shields.io/docker/v/unitystation/central-command?sort=date)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/38cce37d4c854ca48645fd5ecc9cae61)](https://www.codacy.com/gh/unitystation/central-command/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=unitystation/central-command&amp;utm_campaign=Badge_Grade)

The all-in-one backend application for [Unitystation](https://github.com/unitystation/unitystation)

## Features

- Account management and user validation.
- Server list management.
- In-game persistence.
- Works cross-fork!
- Modular architecture.

## Development guide

### Environment setup

Copy `example.env` to `.env` and customize it. You can then start development by either using docker or running the project locally.

### Setting up python to run the project locally

You will need python 3.12+

<details>
<summary>Extra steps if don't want to install poetry globally for some reason</summary>

#### Install venv (only first time or after updating sytem python version)

```sh
python -m venv .venv
```

#### Activate venv on Linux

```sh
. .venv/bin/activate
```

#### Activate venv on Windows

```bat
.venv\Scripts\activate
```

</details>

#### Dependency installation

Install poetry to manage dependencies and update pip

```sh
pip install -U pip poetry
```

Install dev dependencies

```sh
poetry install
```

#### Start the server

from the src folder run
```sh
python manage.py runserver
```

#### pre-commit

pre-commit is a git hook which runs every time you make a commit to catch linting and formatting errors early.  

```sh
pre-commit install
```

> Hint: if the world is on fire, production servers down, clown at your doorstep and you don't have time to make linters happy, add `-n` to `git commit` command (CI will still be mad though).

### Setting up Docker

Docker (with help of compose) lets you launch entire project including database locally without installing anything.

1- To get started with docker, install it from [here](https://docs.docker.com/get-docker/) and (optionally) install [docker engine](https://docs.docker.com/engine/install/).

2- Launch project by running `docker compose -f dev-compose.yml up --build`.

### Try it out

After everything is done, you can access the web UI at http://localhost:8000/. Here you will see the automatic documentation for the API and you can test out the API end points.

Some other useful links:
- http://localhost:8000/admin -> View all accounts and edit existing ones.
- http://localhost:8000/accounts/register -> Create an account.
- http://localhost:8000/accounts/login-credentials -> Test loging in with a username and password.
- http://localhost:8000/accounts/login-token -> Test loging in with a token (see admin page if you lost the token after login with credentials).

You can also use [Bruno](https://www.usebruno.com/) (a Postman alternative) to test out the API. 
The Bruno project is included in the repository and you can find it in the 'api-collection' folder in the root of the repository.
