FROM python:3.7-alpine

# Set a PyPI mirror for Pipenv. Useful for local caching via devpi or similar
ARG PIPENV_PYPI_MIRROR=https://pypi.python.org/simple

# Disable buffering on writing to stdout/stderr. This is to avoid loss of logs in
# the event of an application crash.
ENV PYTHONUNBUFFERED 1
# Disable Pipenv's spinner to stop it from filling logs with garbage
ENV PIPENV_NOSPIN=1


RUN apk update \
  # psycopg2 dependencies
  && apk add gcc python3-dev musl-dev \
  && apk add postgresql-dev \
  # Pillow dependencies
  && apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev diffutils \
  # CFFI dependencies
  && apk add libffi-dev py-cffi \
  # Jupyter dependencies
  && apk add build-base \
  # Ops tools
  && apk add vim curl \
  && addgroup -S django \
  && adduser -h /home/django -S -G django django


# Install pipenv globally
RUN pip install pipenv==2018.11.26
COPY ./backend /app
WORKDIR /app

# Install dependencies system-wide
RUN pipenv --bare install --system --deploy --ignore-pipfile

COPY ./docker/production/backend/gunicorn.sh /gunicorn.sh
RUN sed -i 's/\r//' /gunicorn.sh \
    && chmod +x /gunicorn.sh \
    && chown django /gunicorn.sh

COPY ./docker/entrypoint_backend.sh /entrypoint.sh
RUN sed -i 's/\r//' /entrypoint.sh \
    && chmod +x /entrypoint.sh \
    && chown django /entrypoint.sh



# Copy the rest of the application data in and set ownership to our newly created user
COPY ./shared/ /app/shared/
RUN chown -R django /app $HOME

USER django

ENTRYPOINT ["/entrypoint.sh"]
CMD ["/gunicorn.sh"]
