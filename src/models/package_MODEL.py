import logging
import requests
import os
from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import jsonify
import json
import time
from .convertData import dictDecimalToInt

UPLOAD_FOLDER = 'static/upload/Broadcast/audience/'

db = SQLAlchemy(current_app)
db_contruct = 'SYS_SHOP_Package'
db_pk = 'id'
date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
timestamps = datetime.now().strftime("%Y%m%d%S%f")



def select_by_all(filter=None):
    sqla = ''
    sqlb = ''
    sqlc = ''
    sql = ''
    sqla = "SELECT * "
    sqla += "FROM {} ". format(db_contruct)
    sqla += "WHERE RECORD_STATUS IN ('N') "
    sqla += "AND ("
    if filter:
        for k, v in filter.items():
            sqlb += " ({0} LIKE '%%{1}%%') OR ".format(k, v)

    sqlc += "AND (RECORD_STATUS IN ('N')) "
    sqlc += " ) "
    sqlc += "ORDER BY {} DESC".format(db_pk, id)
    sql = "{} {} {}".format(sqla, sqlb[:-3], sqlc)
    print('----------------------------------------------------------------------')
    print('select_by_all : ', sql)
    print('----------------------------------------------------------------------')
    sql_debug(sql)
    try:
        result = db.engine.execute(sql)
        result_data = [dictDecimalToInt(dict(r)) for r in result]
        if(len(result_data) > 0):
            return jsonify(result_data)
        else:
            return None
    except:
        return None


def select_by_filter(filter=None):
    sql = " SELECT * "
    sql += " FROM {} ". format(db_contruct)
    sql += "WHERE RECORD_STATUS IN ('N')"
    if filter:
        for k, v in filter.items():
            print(k)
            if k == 'last_date_start':
                sql += " AND LAST_DATE >= '{1}' ".format(k, v)
            elif k == 'last_date_end':
                sql += " AND LAST_DATE <= '{1}' ".format(k, v)
            elif k == 'create_date_start':
                sql += " AND CREATE_DATE >= '{1}' ".format(k, v)
            elif k == 'create_date_end':
                sql += " AND CREATE_DATE <= '{1}' ".format(k, v)
            elif k == 'id' and v != '':
                sql += " AND id = '{1}' ".format(k, v)    
            else:
                sql += " AND {0} LIKE '%%{1}%%' ".format(k, v)
    sql += "ORDER BY {} DESC".format(db_pk, id)
    print('----------------------------------------------------------------------')
    print('select_by_filter : ', sql)
    print('----------------------------------------------------------------------')
    sql_debug(sql)
    try:
        result = db.engine.execute(sql)
        result_data = [dictDecimalToInt(dict(r)) for r in result]
        if(len(result_data) > 0):
            return jsonify(result_data)
        else:
            return None
    except:
        return None
def get_user_by_id(id):
    sql = "SELECT id, userName, role FROM users WHERE RECORD_STATUS IN ('N') AND id = '{}'".format(id)
    try:
        result = db.engine.execute(sql)
        result_data = [dictDecimalToInt(dict(r)) for r in result]
        if len(result_data) > 0:
            return result_data[0]
        else:
            return None
    except:
        return None
 
def login(userName=None, password=None):
    sql = " SELECT id, userName, role FROM users "
    sql += " WHERE RECORD_STATUS IN ('N')"
    sql += " AND userName = '{}' AND passwd = '{}' ".format(userName, password)
    print('----------------------------------------------------------------------')
    print('login : ', sql)
    print('----------------------------------------------------------------------')
    sql_debug(sql)
    try:
        result = db.engine.execute(sql)
        result_data = [dictDecimalToInt(dict(r)) for r in result]
        if len(result_data) > 0:
            user = result_data[0]
            return user  # ส่งข้อมูลผู้ใช้พร้อม role
        else:
            return None
    except:
        return None



def select_by_id(id=None):
    sql = " SELECT * "
    sql += " FROM {} ". format(db_contruct)
    sql += " WHERE RECORD_STATUS IN ('N')"
    sql += "AND {} IN ('{}') ".format(db_pk, id)
    print('----------------------------------------------------------------------')
    print('select_by_id : ', sql)
    print('----------------------------------------------------------------------')
    sql_debug(sql)
    try:
        result = db.engine.execute(sql)
        result_data = [dictDecimalToInt(dict(r)) for r in result]
        if(len(result_data) > 0):
            return jsonify(result_data[0])
        else:
            return None
    except:
        return None


def insert(filter=None):
    
    print('insert filter : ', filter)
    sql_fields = ''
    sql_value = ''
    user = ''
    if filter:
        for k, v in filter.items():
            if not v is None:
                sql_fields += " {}, ".format(k)
                sql_value += " '{}', ".format(v)
                if k == 'LAST_USER':
                    user = v
    sql_fields += " RECORD_STATUS, CREATE_DATE, LAST_DATE "
    sql_value += " 'N', '{}', '{}' ".format(date_now, date_now)
    sql = "INSERT INTO {} ({}) VALUES ({})". format(
        db_contruct, sql_fields, sql_value)
    print('----------------------------------------------------------------------')
    print('insert : ', sql)
    print('----------------------------------------------------------------------')
    sql_debug(sql)

    try:
        return db.engine.execute(sql)
    except:
        return None
    
def register(filter=None):
    print('insert filter : ', filter)
    sql_fields = ''
    sql_value = ''
    if filter:
        for k, v in filter.items():
            if v is not None:
                sql_fields += " {}, ".format(k)
                sql_value += " '{}', ".format(v)
    if 'role' not in filter:
        filter['role'] = 'user'  # กำหนด role เริ่มต้นเป็น 'user'

    sql_fields += " RECORD_STATUS, CREATE_DATE, LAST_DATE "
    sql_value += " 'N', '{}', '{}' ".format(date_now, date_now)
    sql = "INSERT INTO {} ({}) VALUES ({})". format(
        'users', sql_fields, sql_value)
    print('----------------------------------------------------------------------')
    print('insert : ', sql)
    print('----------------------------------------------------------------------')
    sql_debug(sql)

    try:
        return db.engine.execute(sql)
    except:
        return None



def update(filter=None, id=None):
    
    print('update id : ', id)
    print('update filter : ', filter)
    user = ''
    sql = " UPDATE {} SET ". format(db_contruct)
    if filter:
        for k, v in filter.items():
            if not v is None:
                print('key : ', k, ' => value : ', v)
                sql += " {0} = '{1}', ".format(k, v)
                if k == 'LAST_USER':
                    user = v
    sql += "LAST_DATE = '{}'".format(date_now)
    sql += "WHERE RECORD_STATUS IN ('N')"
    sql += "AND {} IN ('{}')".format(db_pk, id)
    print('----------------------------------------------------------------------')
    print('Update : ', sql)
    print('----------------------------------------------------------------------')
    sql_debug(sql)
    try:
        return db.engine.execute(sql)
    except:
        return None

def delete(id=None, user=None):
    
    print('Delete id : ', id)
    sql = " UPDATE {} SET ". format(db_contruct)
    sql += "RECORD_STATUS = 'D' , "
    sql += "LAST_USER = '{}' , ".format(user)
    sql += "LAST_DATE = '{}' ".format(date_now)
    sql += "WHERE RECORD_STATUS IN ('N')"
    sql += "AND {} IN ('{}')".format(db_pk, id)
    print('----------------------------------------------------------------------')
    print('delete : ', sql)
    print('----------------------------------------------------------------------')
    sql_debug(sql)
    try:
        return db.engine.execute(sql)
    except:
        return None


def sql_debug(response):
    # print('sql_debug', response)
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)-8s %(message)s' + response,
                        datefmt='%a, %d %b %Y %H:%M:%S', filename='Logs/Log.log')
    
def get_all_users():
    sql = "SELECT * FROM users WHERE RECORD_STATUS IN ('N')"
    try:
        result = db.engine.execute(sql)
        result_data = [dictDecimalToInt(dict(r)) for r in result]
        return result_data
    except:
        return None

def add_user(data):
    sql_fields = ', '.join(data.keys())
    sql_values = ', '.join(["'{}'".format(v) for v in data.values()])
    sql = f"INSERT INTO users ({sql_fields}, RECORD_STATUS, CREATE_DATE, LAST_DATE) VALUES ({sql_values}, 'N', '{date_now}', '{date_now}')"
    try:
        db.engine.execute(sql)
    except:
        return None

def edit_user(id, data):
    sql = "UPDATE users SET "
    sql += ", ".join([f"{k} = '{v}'" for k, v in data.items()])
    sql += f", LAST_DATE = '{date_now}' WHERE id = {id} AND RECORD_STATUS = 'N'"
    try:
        db.engine.execute(sql)
    except:
        return None

def delete_user(id, last_user):
    sql = f"UPDATE users SET RECORD_STATUS = 'D', LAST_USER = '{last_user}', LAST_DATE = '{date_now}' WHERE id = {id} AND RECORD_STATUS = 'N'"
    try:
        db.engine.execute(sql)
    except:
        return None
