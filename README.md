# unitystation_auth

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/83ff59655dfa42509cc61cd9c007162a)](https://app.codacy.com/gh/unitystation/unitystation_auth?utm_source=github.com&utm_medium=referral&utm_content=unitystation/unitystation_auth&utm_campaign=Badge_Grade_Settings)

### Development guide
#### Setting up Docker
TODO

#### Setting up pre-commit
This repository uses pre-commit hook which runs every time you make a commit to catch linting and formatting errors early.  
To enable pre-commit, install it with pip: `pip install -U pre-commit`  
After package installation, install hook running `pre-commit install` inside of project directory.
> Hint: if the world is on fire, production servers down, clown hacks your door and you don't have time to make linters happy, you can add `-m` to `git commit` command.
