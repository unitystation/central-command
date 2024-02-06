FROM python:3.11-alpine3.19

# in order:
# proper stdout flushing for alpine
# no .pyc files
# do not store pip cache
# do not check pip version
# do not yell about root user
ENV PYTHONUNBUFFERED=yes \
    PYTHONDONTWRITEBYTECODE=yes \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_ROOT_USER_ACTION=ignore

WORKDIR /src

COPY poetry.lock pyproject.toml ./

RUN : \
    # psycopg runtime dep
    && apk add --no-cache libpq \
    && pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --only main

COPY src .

# I'm too dumb to make user permissions over shared volumes work
# RUN : \
#     && addgroup -S unitystation \
#     && adduser -S central_command -G unitystation \
#     && chown -R central_command:unitystation /src
#
# USER central_command

RUN : \
    && mkdir /home/website \
    && mkdir /home/website/statics \
    && mkdir /home/website/media \
    && mkdir /home/website/logs

# removes \r from script and makes it executable.
# both of these are caused by windows users touching file and not configuring git properly
RUN : \
    && sed -i 's/\r//g' entrypoint.sh \
    && chmod +x entrypoint.sh

RUN crontab -l | { cat; echo "* * * * * python /src/manage.py send_queued_mail >> /home/website/logs/send_mail.log 2>&1"; } | crontab -

ENTRYPOINT ["./entrypoint.sh"]
