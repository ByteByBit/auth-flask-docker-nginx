###########
# BUILDER #
###########

# pull official base image
FROM python:3.8.1-slim-buster as builder

# set work directory
WORKDIR /usr/src/auth

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc

# lint
RUN pip install --upgrade pip
RUN pip install flake8
COPY . /usr/src/auth/
RUN flake8 --ignore=E501,F401,E402,E722,W503,E203,W504 .

# install python dependencies
COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/auth/wheels -r requirements.txt


#########
# FINAL #
#########

# pull official base image
FROM python:3.8.1-slim-buster

# create directory for the auth user
RUN mkdir -p /home/auth

# create the auth user
RUN addgroup --system auth && adduser --system --group auth


# create the appropriate directories
ENV HOME=/home/auth
ENV AUTH_HOME=/home/auth
# RUN mkdir $AUTH_HOME
WORKDIR $AUTH_HOME

# install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends netcat
COPY --from=builder /usr/src/auth/wheels /wheels
COPY --from=builder /usr/src/auth/requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache /wheels/*

# copy entrypoint.sh
# COPY ./entrypoint.sh $AUTH_HOME

# copy project
COPY . $AUTH_HOME

# chown all the files to the auth user
RUN chown -R auth:auth $AUTH_HOME

# change to the app user
USER auth

# run entrypoint.sh
ENTRYPOINT ["/home/auth/src/entrypoint.sh"]
