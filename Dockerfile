FROM openlabs/docker-wkhtmltopdf:latest
MAINTAINER Sharoon Thomas <sharoon.thomas@openlabs.co.in>

# Install dependencies for running web service
RUN apt-get install -y python-pip
RUN pip install werkzeug executor gunicorn

ADD app.py /app.py
EXPOSE 80

ENTRYPOINT ["usr/local/bin/gunicorn"]

# Show the extended help
CMD ["-b", "0.0.0.0:80", "--log-file", "-", "app:application"]
