from flask import Blueprint, jsonify, request
from db import Session, Cache
from db.family import Caretaker, Family, Patient
import string
import random

def random_key(N):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))

login_blueprint = Blueprint("login", __name__)

@login_blueprint.route('/login', methods=['POST'])
def login():
    session = Session()
    data = request.json

    if data["type"] == "creds":
        u = session.query(Caretaker).filter_by(name = data["name"]).first()
        if u == None:
            return jsonify({"message" : "name not found"}), 400

        if u.password != data["password"]:
            return jsonify({"message" : "wrong password"}), 400

        key = random_key(128)
        Cache[key] = {
            "family_id": u.family_id,
            "type": 1,
            "id": u.id
        }

        return jsonify({"token":key}), 200
    else:
        f = session.query(Family).filter_by(id = data["family_id"]).first()
        if f == None:
            return jsonify({"message":"not found"}), 400

        u = Patient(name = data["name"], img = data["img"], family_id = f.id)
        session.add(u)
        session.commit()

        key = random_key(128)
        Cache[key] = {
            "family_id": u.family_id,
            "type": 0,
            "id": u.id
        }

        return jsonify({"token":key}), 200


@login_blueprint.route('/dbg_register_ct', methods=['POST'])
def dbg_register_ct():
    data = request.json
    session = Session()

    u = Caretaker(name = data["name"], password = data["password"], family_id = data["family_id"])
    session.add(u)
    session.commit()
    print (u, u.id)

    return "ok"

@login_blueprint.route('/dbg_register_fm', methods=['POST'])
def dbg_register_fm():
    session = Session()

    u = Family()
    session.add(u)
    session.commit()
    print (u, u.id)
    return "ok"
