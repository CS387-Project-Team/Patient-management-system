from flask import flash, g, Response, jsonify, render_template, redirect, url_for
import application
from application import default, my_jsonify
import datetime
from pandas import DataFrame

def show_stuff():
    data = {}

    conn = application.connect()
    db = conn.cursor(cursor_factory=application.DictCursor)

    #doctors
    sql = '''select patient_id, id as person_id, name, username
          from person natural join patient
          order by patient_id'''
    db.execute(sql)
    rows = db.fetchall()
    data['patients'] = my_jsonify(rows)

    #rooms/ward
    sql = '''select distinct(type) from room'''
    db.execute(sql)
    rows = db.fetchall()
    data['rooms'] = my_jsonify(rows)

    #num_beds
    sql = '''select type, count(bed_no) as cnt from bed group by type'''
    db.execute(sql)
    rows = db.fetchall()
    data['beds'] = my_jsonify(rows)

    conn.close()
    return render_template('beds/allot_beds.html', data=data)

def allot_beds(data):
	pass



