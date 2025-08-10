FROM python:3.12-alpine3.20

ENV PYTHONUNBUFFERED=yes \
    PYTHONDONTWRITEBYTECODE=yes \
    UV_LINK_MODE=copy

WORKDIR /src

RUN --mount=from=ghcr.io/astral-sh/uv:0.4.24,source=/uv,target=/bin/uv \
    --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    # psycopg runtime dep
    apk add --no-cache libpq \
    # export requirements from uv.lock since uv does not support sync withour venv
    && uv export --frozen --format requirements-txt --no-dev --quiet | uv pip install --system -r -

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
