from flask import Blueprint, jsonify
from db.user import User
from db import Session, Cache

test_blueprint = Blueprint('test', __name__)

@test_blueprint.route('/')
def test_index():
    session = Session()
    q = session.query(User).filter_by(name = 'misu').first()

    msg = "not found"
    if q == None:
        session.add(User(name = "misu"))
        session.commit()
    else:
        msg = str(q)

    if "cached" not in Cache:
        Cache["cached"] = True
    else:
        msg += " cached"

    return jsonify({'message': msg})
