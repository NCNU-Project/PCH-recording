#!/bin/env python3
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://kamailio:kamailiorw@10.22.22.158:3306/kamailio'

db = SQLAlchemy(app)
db.init_app(app)

@app.route("/success_call")
def success_call():
    sql = """
    select
        callid, src_user, dst_user, start_time - ring_time as ring_time, duration, CONCAT(src_user, '-', dst_user, '-', callid, '-', DATE_FORMAT(time, '{date_format}'), '-mix.wav') as filename
    from acc 
        INNER JOIN acc_cdrs USING (callid)
    WHERE method = 'INVITE';
    """.format(date_format='%%Y-%%m-%%d-%%H-%%k-%%s')
    success_calls = db.engine.execute(sql)
    print(success_calls)
    fieldsMap = {"start_time": "通話開始時間", "end_time": "通話結束時間", "ring_time": "響鈴時長", "duration": "總通話時長"}
    queryItems = ["start_time", "end_time", "ring_time", "duration"]
    tableSchema = fieldsMap.keys()
    htmlTableHeader = fieldsMap.values()

    for row in success_calls:
        print(row)
    return "123"
    # return render_template('table.tmpl', rows=rawData)

@app.route("/unsuccess_call")
def index():
    connection = db.session.connection()
    fieldsMap = {"start_time": "通話開始時間", "end_time": "通話結束時間", "ring_time": "響鈴時長", "duration": "總通話時長"}
    queryItems = ["start_time", "end_time", "ring_time", "duration"]
    tableSchema = fieldsMap.keys()
    htmlTableHeader = fieldsMap.values()

    result = connection.execute(text("select {} from acc_cdrs;".format(", ".join(queryItems))).execution_options(autocommit=True))
    rawData = [htmlTableHeader]

    for row in result:
        rawData.append([row[0].strftime("%m/%d/%Y, %H:%M:%S"), row[1].strftime("%m/%d/%Y, %H:%M:%S"), (str)(row[0]- row[2]), row[3]])

    return render_template('table.tmpl', rows=rawData)