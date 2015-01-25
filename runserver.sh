#!/bin/bash
gunicorn --workers=4 --bind=0.0.0.0:8000 mooc.wsgi:application
#gunicorn --bind=0.0.0.0:8000 mooc.wsgi:application
