from flask import flash, g, Response, jsonify, render_template, redirect, url_for
import application
from application import default, my_jsonify
import datetime
from pandas import DataFrame

def get_tests():
    data = {}
    conn = application.connect()
    db = conn.cursor(cursor_factory=application.DictCursor)
    # appointments and prescription
    sql = '''WITH pt(patient_id) as
                (select patient_id
                from patient
                where patient.id = %s)
            select name as test, result_file , comments, dat
            from (takes natural join pt natural join test) as foo'''
    db.execute(sql, (g.user.get('id'),))
    rows = db.fetchall()
    data['tests'] = my_jsonify(rows)
    conn.close()
    print(data)
    return render_template('tests/tests.html', data=data)

def get_available_slots(date_str):
    data = {}
    if date_str == None:
        date_str = "2021-04-21"
    # date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date
    conn = application.connect()
    db = conn.cursor(cursor_factory=application.DictCursor)
    sql = '''select doctor.id, doctor.name, doctor.speciality, start_time, %s as date 
            from doctor_room_slot as drs, (doctor join person on doc_id=id) as doctor
            where drs.doc_id = doctor.id and dat = %s and not exists (
                select * from meet
                where drs.doc_id = doctor.id and dat = %s and meet.start_time = drs.start_time
            )'''
    db.execute(sql, (date_str, date_str, date_str,))
    rows = db.fetchall()
    df = DataFrame(rows)
    if rows == []:
        return jsonify({'msg':'No data found'})
    df.columns = rows[0].keys()
    df = df.groupby('id', as_index=False).agg({'name':'first', 'speciality':'first', 'date':'first', 'start_time': lambda x: list(x)})
    conn.close()
    data['slots'] = df.to_dict(orient='records')
    data['today'] = date_str
    print(data)
    return render_template('appointments/available_slots.html', data=data) #jsonify(df.to_dict(orient='records'))

def confirm_booking(request):
    data = {}
    data['doctor_name'] = request.get('doctor_name')
    data['doctor_id'] = int(request.get('doctor_id'))
    data['date'] = request.get('date')
    data['time'] = request.get('time')
    return render_template('appointments/confirm_booking.html', data=data)

def book_appointment(request):
    print(request)
    doctor_id = int(request.get('doctor_id'))
    date = request.get('date')
    time = request.get('time')
    appo_type = request.get('type')
    complaint = request.get('complaint')
    print(request)
    try:
        followup = int(request.get('followup'))
    except:
        followup = 0
    try:
        patient_id = int(request.get('patient_id'))
    except:
        patient_id = -1
    user_id = g.user['id']
    conn = application.connect()
    db = conn.cursor(cursor_factory=application.DictCursor)
    try:
        if followup == 0:
            sql = '''select 1+max(patient_id) as new_id
                    from patient'''
            db.execute(sql)
            row = db.fetchone()
            patient_id = row['new_id']
            sql = '''insert into patient(id, patient_id)
                    values (%s, %s);'''
            db.execute(sql, (user_id, patient_id,))
        else:
            assert patient_id >= 0, 'invalid patient id'
            sql = '''select dat, start_time from meet
                    where patient_id = %s
                    order by dat desc, start_time desc
                    limit 1'''
            db.execute(sql, (patient_id,))
            row = db.fetchone()
            parent_appo_datetime = datetime.datetime.strptime(row['dat'].isoformat() + ' ' + row['start_time'].isoformat(), '%Y-%m-%d %H:%M:%S')
            assert parent_appo_datetime < datetime.datetime.now(), 'attempting to book a follow up for an appointment which is yet to take place'
        
        assert patient_id >= 0, "invalid patient id"
        sql = '''select 1+max(app_id) as new_id
                from appointment'''
        db.execute(sql)
        row = db.fetchone()
        app_id = row['new_id']
        sql = '''insert into appointment(app_id, type)
                values (%s, %s);'''
        appo_datetime = datetime.datetime.strptime(date + ' ' + time, '%Y-%m-%d %H:%M:%S')
        # To uncomment this when database updates doctor_room_slot
        # assert appo_datetime >= datetime.datetime.now() and appo_datetime.datetime.date <= datetime.date.today()+datetime.timedelta(days=application.MAX_BOOKING_RANGE), 'invalid date for booking a new appointment'
        db.execute(sql, (app_id, appo_type,))
        sql = '''insert into meet(app_id, patient_id, doc_id, dat, start_time, patient_complaint)
                values (%s, %s, %s, %s, %s, %s);'''
        db.execute(sql, (app_id, patient_id, doctor_id, date, time, complaint,))
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)
        conn.rollback()
        conn.close()
        return jsonify({'status':'Failed to book a new appointment', 'code':401})    
    flash('Apoointment booked successfully!', 'success')
    return redirect(url_for('get_appointments')) #render_template('appointments/appointments.html') #jsonify({'status':'Successfully booked a new appointment', 'code':200})


def cancel_appointment(request):
    app_id = int(request.get('app_id'))
    patient_id = int(request.get('patient_id'))
    conn = application.connect()
    db = conn.cursor(cursor_factory=application.DictCursor)
    try:
        
        sql = '''delete from meet
                where app_id = %s returning *;'''
        db.execute(sql, (app_id,))
        deleted_meet = db.fetchone() 
        if deleted_meet is None:
            raise Exception('no appointment deleted')
        # assert datetime.datetime.strptime(deleted_meet['dat'].isoformat() + ' ' + deleted_meet['start_time'].isoformat(), '%Y-%m-%d %H:%M:%S') > datetime.datetime.now(), 'attempting to cancel an appointment which has taken place'
        sql = '''delete from appointment
                where app_id = %s;'''
        db.execute(sql, (app_id,))
        sql = '''select * from meet
                where patient_id = %s;'''
        db.execute(sql, (patient_id,))
        row = db.fetchone()
        if row is None:
            sql = '''delete from patient
                    where patient_id = %s;'''
            db.execute(sql, (patient_id,))
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)
        conn.rollback()
        conn.close()
        return jsonify({'status':'Failed to cancel appointment', 'code':401})    
    flash('Apoointment cancelled successfully!', 'danger')
    return redirect(url_for('get_appointments'))