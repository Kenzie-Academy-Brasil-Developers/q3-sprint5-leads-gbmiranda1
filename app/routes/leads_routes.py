from turtle import pos
from flask import Blueprint
from app.controllers.leads_controller import delete_leads, get_leads, post_leads, update_lead, delete_leads

bp_leads = Blueprint("bp_leads", __name__, url_prefix="/leads")

bp_leads.get("")(get_leads)
bp_leads.post("")(post_leads)
bp_leads.patch("")(update_lead)
bp_leads.delete("")(delete_leads)