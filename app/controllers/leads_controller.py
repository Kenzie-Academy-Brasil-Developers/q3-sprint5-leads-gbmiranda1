from datetime import datetime
from http import HTTPStatus
import re
from flask import request, jsonify
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError, NoResultFound
from app.configs.database import db

from app.models.leads_model import LeadsModel

request_keys = ["name", "email", "phone"]

def get_leads():
    leads = (
        LeadsModel
        .query
        .order_by(desc(LeadsModel.visits))
        .all()
    )
    result = []
    for leads in leads:
        leads = leads.__dict__
        leads.pop('_sa_instance_state', None)
        result.append(leads)

    if not result:
        return jsonify({"error": "no results"}), 404

    return jsonify({"leads_card": result}), HTTPStatus.OK


def phoneVerify(data):
  regex = r"(\(\d{2}\))(\d{5}\-\d{4})"
  phone_verification = re.fullmatch(regex, data["phone"])

  if not phone_verification:
    raise ValueError

def typeVerify(data):
    for value in list(data.values()):
      if type(value) != str:
        raise TypeError

def post_leads():
    data = request.get_json()
    
    try:

        phoneVerify(data)
        typeVerify(data)

        leads = LeadsModel(**data)
        db.session.add(leads)
        db.session.commit()
        return jsonify({
            "name": leads.name,
            "email": leads.email,
            "creation_date": leads.creation_date,
            "last_visit": leads.last_visit,
            "phone": leads.phone,
            "visits": leads.visits
        }), HTTPStatus.CREATED
    except IntegrityError:
      return jsonify({"error": "already registered number or email"}), HTTPStatus.CONFLICT
    except ValueError: 
      return jsonify({"error": "format required (xx)xxxxx-xxxx."}), HTTPStatus.BAD_REQUEST
    except TypeError:
      return jsonify({"error": "values ​​must be string type"}), HTTPStatus.BAD_REQUEST
    except KeyError:
      return {
               "error": "incorrect keys",
               "accept": [
               "name",
               "email",
               "phone"
               ],
               "received": list(data.keys())
            }, HTTPStatus.BAD_REQUEST

def update_lead():
    data = request.get_json()

    try:
        typeVerify(data)

        leads = LeadsModel.query.filter_by(email=data["email"]).one()

        setattr(leads, "visits", (leads.__dict__["visits"]+1))
        setattr(leads, "last_visit", datetime.now())

        db.session.add(leads)
        db.session.commit()

        return jsonify({}), HTTPStatus.NO_CONTENT

    except NoResultFound:
        return jsonify({"error": "not found"}), HTTPStatus.NOT_FOUND
    except TypeError:
      return jsonify({"error": "values ​​must be string type"}), HTTPStatus.BAD_REQUEST
    except KeyError:
      return {
               "error": "incorrect keys",
               "accept": [
               "email",
               ],
               "received": list(data.keys())
            }, HTTPStatus.BAD_REQUEST

def delete_leads():
    data = request.get_json()

    try:
        typeVerify(data)

        leads = LeadsModel.query.filter_by(email=data["email"]).one()

        db.session.delete(leads)
        db.session.commit()

        return jsonify({}), HTTPStatus.NO_CONTENT

    except NoResultFound:
        return jsonify({"error": "not found"}), HTTPStatus.NOT_FOUND
    except TypeError:
      return jsonify({"error": "values ​​must be string type"}), HTTPStatus.BAD_REQUEST
    except KeyError:
      return {
               "error": "incorrect keys",
               "accept": [
               "email",
               ],
               "received": list(data.keys())
            }, HTTPStatus.BAD_REQUEST