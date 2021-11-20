# Central Command
![Docker Image Version (latest by date)](https://img.shields.io/docker/v/unitystation/central-command?sort=date)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/38cce37d4c854ca48645fd5ecc9cae61)](https://www.codacy.com/gh/unitystation/central-command/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=unitystation/central-command&amp;utm_campaign=Badge_Grade)

The all-in-one backend application for [Unitystation](https://github.com/unitystation/unitystation)

### Features
- Account managment and user validation.
- Server list managment.
- In-game persistence.
- Works cross-fork!
- Modular architecture.

### Development guide
#### Setting up Docker
TODO

#### Setting up pre-commit
This repository uses pre-commit hook which runs every time you make a commit to catch linting and formatting errors early.  
To enable pre-commit, install it with pip: `pip install -U pre-commit`  
After package installation, install hook running `pre-commit install` inside of project directory.
> Hint: if the world is on fire, production servers down, clown hacks your door and you don't have time to make linters happy, you can add `-n` to `git commit` command.
