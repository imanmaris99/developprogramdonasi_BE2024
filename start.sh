#!/bin/bash
poetry run gunicorn -w 4 -b 0.0.0.0:$PORT app:app
