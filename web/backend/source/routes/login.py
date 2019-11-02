from flask import Blueprint, jsonify, request
from flask_login import LoginManager, current_user, login_user, logout_user
from db.user import User

login_manager = LoginManager()

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

login_blueprint = Blueprint('login', __name__)

@login_blueprint.route('/login', methods = ['POST'])
def login_route():
    if current_user.is_authenticated:
        return jsonify({"message" : "already authenticated"}), 400

    username = request.json["username"]
    password = request.json["password"]

    user = User.query.filter_by(name = username).first()
    if user == None:
        return jsonify({"message" : "user not found"}), 400

    if user.check_password(password):
        login_user(user)
        return jsonify({"message" : "success"}), 200

    return jsonify({"message" : "wrong password"}), 400

@login_blueprint.route('/logout')
def logout_route():
    if not current_user.is_authenticated:
        return jsonify({"message" : "you must be logged in"}), 400

    logout_user()
    return jsonify({"message" : "success"}), 200
