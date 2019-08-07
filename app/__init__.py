from flask import Flask

from app import config


def create_app(config_name=config.BaseConfig):
    """
    Typical app factory for flask instance
    :param config_name: config file name
    :return: flask app instance
    """
    app = Flask(__name__)
    app.config.from_object(config_name)

    return app

