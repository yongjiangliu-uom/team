from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

from .extensions import db
from .models import User

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

def _get_json():
    data = request.get_json(silent=True)
    return data or {}

@auth_bp.post("/register")
def register():
    data = _get_json()
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not email or not password:
        return jsonify({"error": "email and password are required"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "email already registered"}), 409

    user = User(
        email=email,
        password_hash=generate_password_hash(password),
        role="consumer",
    )
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "registered", "user": user.to_public_dict()}), 201

@auth_bp.post("/login")
def login():
    data = _get_json()
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not email or not password:
        return jsonify({"error": "email and password are required"}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"error": "invalid credentials"}), 401

    # identity 里放 user_id，后面取出来做权限控制
    token = create_access_token(identity=str(user.id), additional_claims={"role": user.role})

    return jsonify({
        "access_token": token,
        "user": user.to_public_dict()
    })