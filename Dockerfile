# Dockerfile from https://learndjango.com/tutorials/django-docker-and-postgresql-tutorial

# Pull base image
FROM python:3.8

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /mytube

# Copy project
COPY . /mytube/

# Install requirements
RUN pip3 install -r requirements.txt
