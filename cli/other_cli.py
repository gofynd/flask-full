import subprocess
import sys
import urllib
import logging
from flask import url_for
from manage import cli
from flask import current_app

logger = logging.getLogger(__name__)


@cli.command()
def lint():
    """Runs code linter."""
    lint = subprocess.call(['flake8', '--ignore=E402', 'app/',
                            'manage.py', 'tests/']) == 0
    if lint:
        print('OK')
    sys.exit(lint)


@cli.command()
def build_docs():
    """Builds docs"""
    subprocess.call(['make', '-C', 'docs/', 'html'])


@cli.command()
def list_routes():
    """Lists all urls available with app"""
    output = []
    for rule in current_app.url_map.iter_rules():
        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)

        methods = ','.join(rule.methods)
        url = url_for(rule.endpoint, **options)
        line = urllib.parse.unquote("{:50s} {:20s} {}".format(rule.endpoint, methods, url))
        output.append(line)

    for line in sorted(output):
        print(line)
