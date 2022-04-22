from flask import Flask
from flask_migrate import Migrate


def init_app(app):

    from app.models.leads_model import LeadsModel

    Migrate(app, app.db)
