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
db_contruct = 'users'
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
    sql = " SELECT * FROM {} WHERE RECORD_STATUS IN ('N')".format(db_contruct)
    if filter:
        for k, v in filter.items():
            if k == 'last_date_start':
                sql += " AND LAST_DATE >= '{}'".format(v)
            elif k == 'last_date_end':
                sql += " AND LAST_DATE <= '{}'".format(v)
            elif k == 'create_date_start':
                sql += " AND CREATE_DATE >= '{}'".format(v)
            elif k == 'create_date_end':
                sql += " AND CREATE_DATE <= '{}'".format(v)
            elif k == 'id' and v:
                sql += " AND id = '{}'".format(v)
            else:
                sql += " AND {} LIKE '%{}%'".format(k, v)
    sql += " ORDER BY {} DESC".format(db_pk)
    try:
        result = db.engine.execute(sql)
        result_data = [dictDecimalToInt(dict(r)) for r in result]
        if len(result_data) > 0:
            return jsonify(result_data)
        else:
            return jsonify([])  # Return an empty list if no results
    except Exception as e:
        print("Error in select_by_filter:", e)
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
    
