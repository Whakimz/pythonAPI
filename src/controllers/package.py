from flask import current_app, render_template, request, redirect
from flask_limiter import Limiter
from ..models import package_MODEL
from flask import jsonify
from google.cloud import storage
from flask import current_app, render_template, request, redirect
from werkzeug.utils import secure_filename
import os
from flask_limiter import Limiter
from PIL import Image
from PIL import ImageOps
import math
from datetime import datetime
import random
import json
import requests
import time


@current_app.route('/package/get', methods=['GET'])
def package():
    filter = request.args.to_dict()
    masterBranch = package_MODEL.select_by_filter(filter)
    if masterBranch:
        return masterBranch
    else:
        response = {
            'status': False,
            'message': 'No data found'
        }
        return jsonify(response), 200
    

@current_app.route('/api/login', methods=['POST'])
def login_get():
    data = request.get_json()
    userName = data.get('userName')
    password = data.get('passwd')
    rs = package_MODEL.login(userName, password)
    if rs:
        return jsonify({'user': rs, 'role': rs['role']})  # ส่ง role กลับไปด้วย
    else:
        response = {
            'status': False,
            'message': 'Invalid username or password'
        }
        return jsonify(response), 200


@current_app.route('/api/register', methods=['POST'])
def register_get():
    data = request.get_json()
    data['role'] = 'user'  # กำหนด role เริ่มต้นเป็น 'user'
    package_MODEL.register(data)
    response = {
        'status': True
    }
    return jsonify(response), 200
    
@current_app.route('/package/add', methods=['POST'])
def package_add():

    if request.method == 'POST':
        bodyObj = request.get_json(silent=True)
        package_MODEL.insert(bodyObj)
        response = {
            'status': True
        }
        return jsonify(response), 200
    
@current_app.route('/package/edit/<int:id>', methods=['POST'])
def package_edit(id):

    if id:

        rs = package_MODEL.select_by_id(id)
        if rs:
            bodyObj = request.get_json(silent=True)
            package_MODEL.update(bodyObj, id)
            response = {
                'status': True
            }
            return jsonify(response), 200
        
@current_app.route('/package/delete/<int:id>', methods=['POST'])
def package_delete(id):

    if id:

        rs = package_MODEL.select_by_id(id)
        print(rs)
        if rs:
            bodyObj = request.get_json(silent=True)
            last_user = bodyObj.get('LAST_USER')
            package_MODEL.delete(id, last_user)
            response = {
                'status': True
            }
            return jsonify(response), 200

@current_app.route('/users/get', methods=['GET'])
def get_users():
    users = package_MODEL.get_all_users()
    if users:
        return jsonify(users)
    else:
        return jsonify({'status': False, 'message': 'No users found'}), 200

@current_app.route('/users/add', methods=['POST'])
def add_user():
    data = request.get_json()
    package_MODEL.add_user(data)
    return jsonify({'status': True}), 200

@current_app.route('/users/edit/<int:id>', methods=['POST'])
def edit_user(id):
    data = request.get_json()
    package_MODEL.edit_user(id, data)
    return jsonify({'status': True}), 200

@current_app.route('/users/delete/<int:id>', methods=['POST'])
def delete_user(id):
    data = request.get_json()
    last_user = data.get('LAST_USER')
    package_MODEL.delete_user(id, last_user)
    return jsonify({'status': True}), 200        