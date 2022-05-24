FROM python

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get -o Acquire::Check-Valid-Until=false -o Acquire::Check-Date=false update -y \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  # psycopg2 dependencies
  && apt-get install -y libpq-dev \
  # Translations dependencies
  && apt-get install -y gettext \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*


WORKDIR /app
COPY ./requirements/base.txt /app
COPY ./requirements/local.txt /app
#RUN pip install --proxy=http://proxy.sld.cu:3128 --use-feature=2020-resolver --no-cache-dir -r local.txt
RUN  pip install --index-url http://nexus.prod.uci.cu/repository/pypi-all/simple --trusted-host nexus.prod.uci.cu --no-cache-dir -r local.txt


COPY . /app

COPY ./runserver.sh /app/runserver.sh
RUN sed -i 's/\r$//g' /app/runserver.sh

# Grant permissions for the entrypoint script to be executable
RUN chmod +x /app/runserver.sh

# Gunicorn
COPY /gunicorn/config.py /etc/gunicorn.py
RUN mkdir -p /app/gunicorn/log


RUN mkdir -p /app/static
# give permission for nginx to read static files
RUN chown -R "$USER":www-data /app/static && chmod -R 0755 /app/static
RUN chown -R "$USER":www-data /app/media && chmod -R 0755 /app/media

EXPOSE 8443

CMD ["/app/runserver.sh"]
