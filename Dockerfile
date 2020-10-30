FROM python:3

#handle envirs
ENV   PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100

# copy django project
WORKDIR /djangoapp
COPY ./unitystation_auth .

#install dependencies
COPY poetry.lock .
COPY pyproject.toml .
RUN pip install poetry
RUN poetry config virtualenvs.create false \
  && poetry install


