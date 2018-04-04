import os

from . import create_app

# Create an application instance that auxiliary processes such as Celery
# workers can use
app = create_app(main=False)
