#!/usr/bin/env bash
su -m www-data -s /bin/bash -c "python3 manage.py run -h 0.0.0.0 -p 8080"