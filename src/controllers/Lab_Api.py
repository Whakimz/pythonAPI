from flask import current_app, render_template, request, redirect
from flask_limiter import Limiter
from ..models import Lab_Api_MODEL
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
from flask import g

@current_app.route('/labApi/get', methods=['GET'])
def labApi_get():
    # ทดสอบ
    print('test')
    filter = request.args.to_dict()
    masterBranch = Lab_Api_MODEL.select_by_filter(filter)
    if masterBranch:
        return masterBranch
    else:
        response = {
            masterBranch : 'Null',
            'status': False,
            'message': 'No data found'
        }
        return jsonify(response), 200


@current_app.route('/labApi/find_advanced', methods=['GET'])
def labApi_find():

    filter = request.args.to_dict()
    return Lab_Api_MODEL.select_by_all(filter)


@current_app.route('/labApi/getID/<int:id>', methods=['GET'])
def labApi_get_id(id):
    response = Lab_Api_MODEL.select_by_id(id)
    return response, 200

@current_app.route('/labApi/add', methods=['POST'])
def labApi_add():

    if request.method == 'POST':
        bodyObj = request.get_json(silent=True)
        Lab_Api_MODEL.insert(bodyObj)
        response = {
            'status': True
        }
        return jsonify(response), 200


@current_app.route('/labApi/edit/<int:id>', methods=['POST'])
def labApi_edit(id):

    if id:

        rs = Lab_Api_MODEL.select_by_id(id)
        if rs:
            bodyObj = request.get_json(silent=True)
            Lab_Api_MODEL.update(bodyObj, id)
            response = {
                'status': True
            }
            return jsonify(response), 200


@current_app.route('/labApi/delete/<int:id>', methods=['POST'])
def labApi_delete(id):

    if id:

        rs = Lab_Api_MODEL.select_by_id(id)
        print(rs)
        if rs:
            bodyObj = request.get_json(silent=True)
            last_user = bodyObj.get('LAST_USER')
            Lab_Api_MODEL.delete(id, last_user)
            response = {
                'status': True
            }
            return jsonify(response), 200
