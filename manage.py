from flask.cli import FlaskGroup
from app import create_app


cli = FlaskGroup(create_app=create_app)

from cli import *

if __name__ == '__main__':
    cli()