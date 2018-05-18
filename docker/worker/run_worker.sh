#!/usr/bin/env bash
su -m www-data -s /bin/bash -c "python3 manage.py celery"
#python3 manage.py celery