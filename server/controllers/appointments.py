from flask import g, Response, jsonify
import application
from application import default, my_jsonify
import datetime
from pandas import DataFrame

def get_available_slots(date_str):
    data = {}
    # date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date
    conn = application.connect()
    db = conn.cursor(cursor_factory=application.DictCursor)
    sql = '''select doctor.id, doctor.name, doctor.speciality, start_time, %s as date 
            from doctor_room_slot, (doctor natural join person) as doctor
            where doc_id = doctor.id and dat = %s and not exists (
                select * from meet
                where doc_id = doctor.id and dat = %s and meet.start_time = doctor_room_slot.start_time
            )'''
    db.execute(sql, (date_str, date_str, date_str,))
    rows = db.fetchall()
    df = DataFrame(rows)
    if rows == []:
        return jsonify({})
    df.columns = rows[0].keys()
    df = df.groupby('id', as_index=False).agg({'name':'first', 'speciality':'first', 'date':'first', 'start_time': lambda x: list(x)})
    conn.close()
    return jsonify(df.to_dict(orient='records'))

def book_appointment(request):
    doctor_id = int(request.get('doctor_id'))
    date = request.get('date')
    time = request.get('time')
    appo_type = request.get('type')
    complaint = request.get('complaint')
    user_id = g.user['id']
    conn = application.connect()
    db = conn.cursor(cursor_factory=application.DictCursor)
    try:
        sql = '''select 1+max(patient_id) as new_id
                from patient'''
        db.execute(sql)
        row = db.fetchone()
        patient_id = row['new_id']
        sql = '''select 1+max(app_id) as new_id
                from appointment'''
        db.execute(sql)
        row = db.fetchone()
        app_id = row['new_id']
        sql = '''insert into patient(id, patient_id)
                values (%s, %s);'''
        db.execute(sql, (user_id, patient_id,))
        sql = '''insert into appointment(app_id, type)
                values (%s, %s);'''
        db.execute(sql, (app_id, appo_type,))
        sql = '''insert into meet(app_id, patient_id, doc_id, dat, start_time, patient_complaint)
                values (%s, %s, %s, %s, %s, %s);'''
        db.execute(sql, (app_id, patient_id, doctor_id, date,time, complaint,))
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)
        conn.rollback()
        conn.close()
        return jsonify({'status':'Failed to book a new appointment', 'code':401})    
    return jsonify({'status':'Successfully booked a new appointment', 'code':200})