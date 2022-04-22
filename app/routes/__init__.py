from flask import Flask
from app.routes.leads_routes import bp_leads

def init_app(app):
    app.register_blueprint(bp_leads)