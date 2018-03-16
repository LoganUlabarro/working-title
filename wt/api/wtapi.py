"""working-title web API."""

from flask import Flask

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

from wt.api import routes
