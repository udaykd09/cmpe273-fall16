# A simple Flask app container.
FROM python:2.7
MAINTAINER  Uday Dungarwal <uday.dungarwal@sjsu.edu>

# Place app in container.
COPY . /opt/www
WORKDIR /opt/www

# Install dependencies.
RUN pip install -r requirements.txt

EXPOSE 80
CMD python app.py
