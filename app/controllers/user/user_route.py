
from flask import Blueprint, json, request, jsonify
from flask_bcrypt import Bcrypt
from app.decorators.role_checker import role_required
from app.models.user import User, db
from app.utils.api_response import api_response
from app.utils.db import db
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from sqlalchemy.exc import SQLAlchemyError

from werkzeug.security import generate_password_hash,check_password_hash
import bcrypt
import re

user_blueprint = Blueprint('user_endpoint', __name__)
bcrypt = Bcrypt()

# ----->>>> ACCESS USER CUSTOMER PAGE ---->>>>>>>

# Registering a new user CUSTOMER-->>>>>
@user_blueprint.route('/register', methods=["POST"])
def create_user():
    
    data = request.get_json()

    # Validate input data
    if not data or not 'email' in data or not 'name' in data or not 'password' in data:
        return api_response(
            status_code=400,
            message='Missing required fields',
            data={}
        )

    email = data['email']
    name = data['name']
    password = data['password']

    # Email format validation
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_regex, email):
        return api_response(
                status_code=400,
                message='Invalid email format',
                data={}
            )  

    # Password complexity validation
    if len(password) < 8:
        return api_response(
            status_code=400,
            message='Password must be at least 8 characters long',
            data={}
        )

    try:
        # Checking if the user already exists
        user_exists = User.query.filter_by(email=email).first()
        if user_exists:
            return api_response(
                status_code=400,
                message='User already registered',
                data={}
            )  


        # Encrypting password with bcrypt
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Creating a new user
        new_user = User(
            email=email,
            name=name,
            role='member',
            password=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()

        # Returning registration data
        registration_data = {
            'id': new_user.id,
            'email': new_user.email,
            'name': new_user.name,
            'role': new_user.role,
            'created_at': new_user.created_at.strftime("%Y-%m-%d %H:%M:%S") if new_user.created_at else None,
            'updated_at': new_user.updated_at.strftime("%Y-%m-%d %H:%M:%S") if new_user.updated_at else None
        }

        return api_response(
            status_code=201,
            message='User-data successfully added',
            data={'user-data': registration_data}
        )
    
    except SQLAlchemyError as e:
        db.session.rollback()  # Rollback the session in case of an error
        return api_response(
            status_code=500,
            message='Failed to add user data',
            data={'error': str(e)}
        )

    except Exception as e:
        return api_response(
            status_code=500,
            message='An unexpected error occurred',
            data={'error': str(e)}
        )


# --->>>> Login Page --->>>>>

@user_blueprint.route('/login', methods=["POST"])
def login_user():
    data = request.get_json()

    try:
        # Checking if the user is registered
        user = User.query.filter_by(email=data['email']).first()
        if user and bcrypt.check_password_hash(user.password, data['password']):
            # Creating JWT token
            access_token = create_access_token(identity=user.id)
            return api_response(
                status_code=200,
                message='Login successfull',
                data={'access_token': access_token}
            )
        else:
            return api_response(
                status_code=401,
                message='Incorrect email or password',
                data={}
            )
    except Exception as e:
        return api_response(
            status_code=500,
            message='Failed during login',
            data={'error': str(e)}
        )

@user_blueprint.route('/profile', methods=["GET"])
@jwt_required()  # Membutuhkan token JWT untuk akses
def user_register():
    try:
        # Mendapatkan identitas pengguna yang saat ini login dari token JWT
        current_user_id = get_jwt_identity()

        # Querying untuk mendapatkan data pengguna yang saat ini login
        user = User.query.filter_by(id=current_user_id).first()

        # Memastikan pengguna ditemukan
        if not user:
            # return jsonify({'error': 'User not found'}), 404
            return api_response(
                status_code=404,
                message='User not found',
                data={}
            )

        # Mengonversi data pengguna ke format JSON
        user_data = {
                'id': user.id,
                'email': user.email,
                'name': user.name,
                'password': user.password,
                'role': user.role,
                'created_at': user.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                'updated_at': user.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        }

        # Mengembalikan data pengguna sebagai JSON
        return api_response(
                status_code=200,
                message='User-Profile successful access',
                data={'access_token': user_data}
            )
    
    except SQLAlchemyError as e:
        # Mengembalikan pesan kesalahan jika ada kesalahan kueri basis data
        # return jsonify({'error': 'Failed to fetch user data', 'message': str(e)}), 500
        return api_response(
            status_code=500,
            message='Failed to fetch user data',
            data={'error': str(e)}
        )

    
@user_blueprint.route('/edit', methods=["PUT"])
@jwt_required()  # Membutuhkan token JWT untuk akses
def update_profile():
    try:
        # Mendapatkan identitas pengguna yang saat ini login dari token JWT
        current_user_id = get_jwt_identity()

        # Mendapatkan data pengguna yang saat ini login
        user = User.query.filter_by(id=current_user_id).first()

        # Memastikan pengguna ditemukan
        if not user:
            # return jsonify({'error': 'User not found'}), 404
            return api_response(
                status_code=404,
                message='User not found',
                data={}
            )

        # Mendapatkan data yang akan diubah dari permintaan
        data = request.json

        # Memperbarui data pengguna
        user.email = data.get('email', user.email)
        user.name = data.get('name', user.name)
        # user.role = data.get('role', user.role)

        # Commit perubahan ke database
        db.session.commit()

        # Mengonversi data pengguna ke format JSON
        user_data = {
                'id': user.id,
                'email': user.email,
                'name': user.name,
                'password': user.password,
                'role': user.role,
                'created_at': user.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                'updated_at': user.updated_at.strftime("%Y-%m-%d %H:%M:%S")
        }

        # Mengembalikan data pengguna sebagai JSON
        return api_response(
                status_code=200,
                message='User-data successfully updated',
                data={'data_updated': user_data}
            )

        # # Mengembalikan pesan sukses
        # return jsonify({'message': 'data user updated successfully'}), 200
    except SQLAlchemyError as e:
        # Mengembalikan pesan kesalahan jika ada kesalahan kueri basis data
        # return jsonify({'error': 'Failed to update profile', 'message': str(e)}), 500
        return api_response(
            status_code=500,
            message='Failed to update profile',
            data={'error': str(e)}
        )


# ->>--->>----->>>>>--ADMIN(Admin Only)-- ACCESS-->>--->>--->>>ADMIN(Admin Only)-- ACCESS----->>>----->>---->>>>>>

@user_blueprint.route('/admin/register', methods=["POST"])
def create_user_admin():
    data = request.get_json()

    required_fields = ['email', 'name', 'role', 'password']
    if not all(field in data for field in required_fields):
        return api_response(
            status_code=400,
            message='Missing required fields',
            data={}
        )

    email = data['email']
    name = data['name']
    role = data['role']
    password = data['password']

    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_regex, email):
        return api_response(
            status_code=400,
            message='Invalid email format',
            data={}
        )

    if len(password) < 8:
        return api_response(
            status_code=400,
            message='Password must be at least 8 characters long',
            data={}
        )

    try:
        user_exists = User.query.filter_by(email=email).first()
        if user_exists:
            return api_response(
                status_code=400,
                message='User already registered',
                data={}
            )

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        new_user = User(
            email=email,
            name=name,
            role=role,
            password=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()

        # Returning registration data
        registration_admin = {
            'id': new_user.id,
            'email': new_user.email,
            'name': new_user.name,
            'role': new_user.role,
            'created_at': new_user.created_at.strftime("%Y-%m-%d %H:%M:%S") if new_user.created_at else None,
            'updated_at': new_user.updated_at.strftime("%Y-%m-%d %H:%M:%S") if new_user.updated_at else None
        }

        return api_response(
            status_code=201,
            message='User successfully added',
            data={'data added': registration_admin}
        )
    except Exception as e:
        db.session.rollback()
        return api_response(
            status_code=500,
            message='Failed to add user',
            data={'error': str(e)}
        )    

@user_blueprint.route('/admin/login', methods=["POST"])
def login_user_admin():
    data = request.get_json()

    try:
        # Checking if the user is registered
        user = User.query.filter_by(email=data['email']).first()
        if user and check_password_hash(user.password, data['password']):
            # Creating JWT token
            access_token = create_access_token(identity=user.id)
            return api_response(
                status_code=200,
                message='User-Admin login successful',
                data={'access_token': access_token}
            )
        else:
            return api_response(
                status_code=401,
                message='Incorrect email or password',
                data={}
            )
    except Exception as e:
        return api_response(
            status_code=500,
            message='Failed during login',
            data={'error': str(e)}
        )
    
@user_blueprint.route('/admin/users', methods=["GET"])
@jwt_required()
@role_required('admin')
def all_user_register():
    try:
        users = User.query.all()
        users_data = []
        for user in users:
            user_data = {
                'id': user.id,
                'email': user.email,
                'name': user.name,
                'password': user.password,
                'role': user.role,
                'created_at': user.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                'updated_at': user.updated_at.strftime("%Y-%m-%d %H:%M:%S") if user.updated_at else None
            }
            users_data.append(user_data)

        # return jsonify(users_data), 200
        return api_response(
            status_code=200,
            message='User-Admin successfully access list all users',
            data={'list_users': users_data}
        )
    
    except SQLAlchemyError as e:
        # return jsonify({'error': 'Failed to fetch user data', 'message': str(e)}), 500
        return api_response(
            status_code=500,
            message='Failed to fetch user data',
            data={'error': str(e)}
        )
    
# >>>>>>>>>>>>>----USER--ADMIN--END---->>>>>>>>>>>>>>

