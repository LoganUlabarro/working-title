"""wt-api config."""
from os import environ
from pathlib import Path

from dotenv import load_dotenv


p = Path(__file__).parent / '.env'
load_dotenv(p)


class Config(object):
    SECRET_KEY = environ.get('SECRET_KEY')
