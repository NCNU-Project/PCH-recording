#!/bin/env python3
from pydoc import plain
from flask import Flask, render_template, send_file, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import json
from glob import glob
import os
from os import path
import urllib.request

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' + os.environ["DATABASE_URI"]
app.config['FILE_ROOT_DIRECTORY'] = os.environ["FILE_ROOT_DIRECTORY"]
db = SQLAlchemy(app)
db.init_app(app)


@app.route("/get_file_by_prefix/<prefix>")
def getFiles(prefix):
    """
    giving the prefix, and searching over the file root directory
    if not found the correspond prefix file, return None
    else return the absoulte path of this file
    """

    file_root = app.config['FILE_ROOT_DIRECTORY']
    sanitized_file_prefix = path.basename(urllib.request.pathname2url(path.normpath(prefix)))

    # the filename at least have a number or a char, otherwize just return None
    if any(c.isalpha() or c.isdigit() for c in sanitized_file_prefix):
        # searching file with the given prefix
        file_canidate = glob(
            '{}*'.format(sanitized_file_prefix), root_dir=file_root)
        if len(file_canidate) and path.isfile(path.join(file_root, file_canidate[0])):
            return send_file(path.join(file_root, file_canidate[0]))

    abort(404)


@app.route("/success_call")
def success_call():
    sql = """
    SELECT
        callid, src_user, dst_user, start_time, end_time, start_time - ring_time as ring_time, duration, CONCAT(src_user, '-', dst_user, '-', callid) as file_prefix
    FROM acc 
        INNER JOIN acc_cdrs USING (callid)
    WHERE method = 'INVITE';
    """
    with db.engine.connect() as connection:
        success_calls = connection.execute(text(sql)).mappings().all()
        fieldsMap = {"callid": "call-id", "src_user": "撥打者", "dst_user": "接收者",
                     "start_time": "通話開始時間", "end_time": "通話結束時間", "ring_time": "響鈴時長(秒)", "duration": "總通話時長(秒)", "file_prefix": "錄音檔"}

        rawData = [fieldsMap.values()]
        for row in success_calls:
            row = dict(row)
            row['file_prefix'] = {
                "val": '/get_file_by_prefix/' + row['file_prefix'], "type": "url"}
            rawData.append(row.values())

    return render_template('table.html', rows=rawData)


@app.route("/unsuccess_call")
def unsuccess_call():
    sql = """
    SELECT
        callid, src_user, dst_user, time, time - ring_time as ring_time
    FROM missed_calls
        INNER JOIN acc_cdrs USING (callid)
    """
    with db.engine.connect() as connection:
        success_calls = connection.execute(text(sql)).mappings().all()
        fieldsMap = {"callid": "call-id", "src_user": "撥打者", "dst_user": "接收者",
                     "time": "通話撥出時間", "ring_time": "響鈴時長(秒)"}

        rawData = [fieldsMap.values()]
        for row in success_calls:
            row = dict(row)
            rawData.append(row.values())

    return render_template('table.html', rows=rawData)


@app.route("/")
def index():
    indexs = ["unsuccess_call", "success_call"]
    return render_template('index.html', rows=indexs)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
