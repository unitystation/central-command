FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /src
WORKDIR /src
ADD src/ /src/
COPY poetry.lock /src/
COPY pyproject.toml /src/
RUN pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install
