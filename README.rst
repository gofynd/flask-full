Flask-Full
**********
.. image:: https://img.shields.io/circleci/project/github/RedSparr0w/node-csgo-parser/master.svg
    :alt: Travis

Flask-Full is a boilerplate framework on top of flask for developing large api backend applications using flask. It has in built support for creating shell commands, celery, websocket, eventlet, mongoengine orm, swagger-ui api docs and sphinx docs.

Usage
-----
Flask-Full requires  minimum **python 3.5**.

Pre-required Setup:

* MacOS/Linux/Windows

* git

* Python3 / pip3 /

* MongoDB

.. code:: shell

    git clone https@github.com:fynd/flask-full.git
    cd flask-full (rename repository directory to required value)
    pip3 install -r requirements.txt

To start server hit

.. code:: shell

    python3 manage.py run -p 8080

Server will start on port 8080. Hitting http://localhost:8080/ping/ on web browser should return {"message": "pong"}.

API Docs are powered by swagger ui and can be viewed by hitting http://localhost:8080/apidocs/ .

To start celery hit

.. code:: shell

    python3 manage.py celery

To start beat hit

.. code:: shell

    python3 manage.py beat

For available commands and options hit

.. code:: shell

    python manage.py



Structure
---------
.. code:: shell

    ├── CHANGES                     Change logs
    ├── README.rst
    ├── manage.py                   Management commands file
    ├── meta.conf                   App meta conf
    ├── requirements.txt            3rd party libraries libraries
    ├── requirements_test.txt       Testing 3rd libraries
    ├── temp                        Temp directory for storing logs
    ├── app
       ├── __init__.py              App starting point
       ├── app.py                   Main blueprint with before and after request handler
       ├── api_info.py              API level constants
       ├── choices.py               CHOICES constant dictionary
       ├── crons.py                 Crons dictionary file
       ├── exceptions.py            Custom exceptions
       ├── stats.py                 API stats
       ├── wsgi.py                  wsgi app
       ├── wsgi_aux.py              wsgi auxilary app
       ├── utils                    Utils
       │   ├── __init__.py
       │   ├── api_caller.py        Wrapper over requests which handles emits blinker signal over call
       │   ├── common_util.py       common utils
       │   ├── json_util.py         contains custom flask encodes
       │   ├── slack_util.py
       └── api
           └── v1
               └── ├── urls.py url routes
                   ├──demo_api  container one demo api


You can also use docker-compose. Hit below command to start server on port 8080.

.. code:: shell

    docker-compose build
    docker-compose up
