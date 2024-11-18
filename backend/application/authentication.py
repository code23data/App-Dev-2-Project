from flask import jsonify, request
from flask import current_app as app
from flask_cors import cross_origin
from werkzeug.security import generate_password_hash, check_password_hash


from .database import db
from .models import User
from flask_jwt_extended import create_access_token
from flask import send_from_directory
import time


@app.route("/register/user", methods=["POST"])
@cross_origin()
def register_user():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    email = request.json.get("email", None)
    print(f"Username : {username} \n Password : {password}")
    print("\n\n\n\n")

    user = User.query.filter_by(username=username).first()
    if user:
        return {"error": f"User with username {username} already exists"}, 409
    hashed_password = generate_password_hash(password, method="pbkdf2:sha256")

    if username and email and password:
        new_user = User(username=username, password=hashed_password, email=email)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User registered successfully"}), 201

    return jsonify({"error": "Insufficient or incorrect credentials"}), 401


@app.route("/register/admin", methods=["POST"])
@cross_origin()
def register_admin():

    username = request.json.get("username", None)
    password = request.json.get("password", None)
    email = request.json.get("email", None)
    print(f"Username : {username} \n Password : {password}")
    print("\n\n\n\n")

    admin = User.query.filter_by(username=username).first()
    if admin:
        return {"error": f"Admin with username {username} already exists"}, 409
    hashed_password = generate_password_hash(password, method="pbkdf2:sha256")

    if username and email and password:
        new_admin = User(
            username=username, password=hashed_password, email=email, isadmin=True
        )
        db.session.add(new_admin)
        db.session.commit()
        return jsonify({"message": "Admin registered successfully"}), 201

    return jsonify({"error": "Insufficient or incorrect credentials"}), 401


@app.route("/login", methods=["POST"])
def user_login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    # email = request.json.get("email", None)
    user = User.query.filter_by(username=username).first()

    # Checking if username and password is valid
    if username and check_password_hash(user.password, password):
        user.lastseen = time.time()
        db.session.commit()
        token = create_access_token(
            identity=user.user_id, additional_claims={"isadmin": user.isadmin}
        )
        return jsonify({**user.to_dict(), "access_token": token}), 200

    return jsonify({"error": "Invalid or incorrect credentials"}), 401


@app.route("/login/admin", methods=["POST"])
def admin_login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    email = request.json.get("email", None)
    user = User.query.filter_by(username=username).first()

    # Checking if username and password is valid
    if username and check_password_hash(user.password, password) and user.isadmin:
        token = create_access_token(
            identity=user.user_id, additional_claims={"isadmin": user.isadmin}
        )
        return jsonify({**user.to_dict(), "access_token": token}), 200

    return jsonify({"error": "Invalid or incorrect credentials"}), 401
