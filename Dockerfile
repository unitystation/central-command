FROM python:3.8
ENV PYTHONUNBUFFERED 1
WORKDIR /src
COPY poetry.lock .
COPY pyproject.toml .
RUN pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install
ADD src/ /src/
ENTRYPOINT ["python", "manage.py", "runserver", "0.0.0.0:8000"]