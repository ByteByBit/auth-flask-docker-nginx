#!/usr/bin/env bash

export FLASK_APP=server.py
export FLASK_DEBUG=1
export APP_CONFIG_FILE=config.py
flask run