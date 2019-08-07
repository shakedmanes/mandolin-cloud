import os


class BaseConfig(object):
    """Default configuration options for flask"""
    SITE_NAME = os.environ.get('APP_NAME', 'mandolin-cloud')
