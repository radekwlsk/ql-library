# User ID for the django user we're creating. The builder can set this to the
# host user's ID to avoid file permissions problems.
ARG USER_ID=1000
# Whether we're running in local development mode
ARG DEV_MODE=0

FROM python:3.9-slim as base

ENV HOME=/home/django
ENV PIPENV_RELEASE=2022.1.8
# Disable buffering on writing to stdout/stderr. This is to avoid loss of logs in
# the event of an application crash.
ENV PYTHONUNBUFFERED=1
# Disable Pipenv's spinner to stop it from filling logs with garbage
ENV PIPENV_NOSPIN=1
# Save the lock file here if this is the first build
ENV BUILD_PIPFILE_LOCK=$HOME/Pipfile.lock.build
# And a location for the application virtualenv based on the above
ENV VIRTUAL_ENV=$HOME/venv
# Add virtualenv bin folder to the PATH
ENV PATH="$HOME/venv/bin:/app:$PATH"
ENV PYTHONPATH="/app:$PYTHONPATH"


FROM base as builder

# Need to redeclare build args due to Dockerfile semantics
ARG USER_ID
ARG DEV_MODE

# Install build dependencies
RUN apt-get -qq update \
    && apt-get -qq -y install \
    # psycopg2 dependencies
    libpq-dev gcc postgresql-client \
    # Pillow dependencies
    libjpeg-dev zlib1g-dev libfreetype6-dev liblcms2-dev libopenjp2-7-dev libtiff-dev tcl8.6-dev tk8.6-dev python3-tk \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get -qq -y clean

# Install pipenv globally
RUN HOME=/tmp pip install --no-cache-dir pipenv==$PIPENV_RELEASE

COPY ./backend/Pipfile ./backend/*.lock $HOME/
WORKDIR $HOME

# Prepare virtualenv and install Python dependencies
RUN python3 -m venv $VIRTUAL_ENV \
    && if [ $DEV_MODE -eq 1 ]; then \
    # dev mode, install dev dependencies
    # We'd like this to fail if the Pipfile.lock is out of date, but also to generate
    # the lockfile if it doesn't exist, which it won't on the first build.
        pipenv install --dev --deploy; \
    else \
    # normal (production) mode, install non-dev dependencies while verifying that
    # Pipfile.lock is up to date. Manually check if Pipfile.lock exists because --deploy
    # will still generate a new one if it's not there.
        [ -f Pipfile.lock ] || { echo 'No Pipfile.lock found' ; exit 1; }; \
        pipenv install --deploy; \
    fi \
    && cp -f Pipfile.lock $BUILD_PIPFILE_LOCK \
    && rm -rf $HOME/.cache/*


FROM base AS final

# Need to redeclare build args due to Dockerfile semantics
ARG USER_ID
ARG DEV_MODE

# Install runtime dependencies and ops tools
RUN apt-get -qq update \
    && apt-get -qq -y install \
    # Shared library for Postgres clients
    libpq5 postgresql-client \
    # Pillow dependencies
    libjpeg62-turbo zlib1g libfreetype6 liblcms2-2 libopenjp2-7 libtiff5 tcl8.6 tk8.6 python3-tk \
    # Translations dependencies
    gettext \
    # Ops tools
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get -qq -y clean


# Install pipenv if we're in dev mode
RUN if [ $DEV_MODE -eq 1 ]; then HOME=/tmp pip install --no-cache-dir pipenv==$PIPENV_RELEASE; fi

# Create the user and group to run the Django application as
RUN addgroup --system --gid $USER_ID django \
    && adduser --system --home $HOME --uid $USER_ID --ingroup django django


# Copy the start scripts, make them executable, and set ownership
COPY --chown=django:django ./docker/scripts/ /
RUN chmod +x /*.sh

# Create the application folder with the right dependencies
RUN mkdir -p /app && chown django /app

# Create a folder to store media in if we're in dev mode
RUN if [ $DEV_MODE -eq 1 ]; then \
        mkdir -p /media && chown django /media; \
    fi

USER django

# Copy the built virtualenv from the builder stage
COPY --from=builder --chown=django:django $VIRTUAL_ENV $VIRTUAL_ENV
COPY --from=builder --chown=django:django $BUILD_PIPFILE_LOCK $BUILD_PIPFILE_LOCK

# Copy the application data in
COPY --chown=django:django ./backend /app/
COPY --chown=django:django ./shared /app/shared/

WORKDIR /app

# Make the runner script executable
RUN chmod +x /app/manage.sh

CMD ["/start-gunicorn.sh"]
