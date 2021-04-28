from flask import g, Response, jsonify, render_template
import application
from application import default, my_jsonify

def get_info():
    data = {}

    conn = application.connect()
    db = conn.cursor(cursor_factory=application.DictCursor)

    #doctors
    sql = '''select name, speciality, experience, opd_charges, ot_charges
          from doctor,person 
          where doc_id = id
          order by speciality asc, name asc'''
    db.execute(sql)
    rows = db.fetchall()
    data['doctors'] = my_jsonify(rows)

    #staff
    sql = '''select role, count(staff_id) as cnt
            from support_staff
            group by role'''
    db.execute(sql)
    rows = db.fetchall()
    data['staff'] = my_jsonify(rows)

    #departments
    sql = '''select speciality, count(doc_id) as cnt
            from doctor
            group by speciality'''
    db.execute(sql)
    rows = db.fetchall()
    data['departments'] = my_jsonify(rows)

    #equipments
    sql = '''select distinct(type) from equipment'''
    db.execute(sql)
    rows = db.fetchall()
    data['equipments'] = my_jsonify(rows)

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
    return render_template('dashboard/generic_info.html',data=data)