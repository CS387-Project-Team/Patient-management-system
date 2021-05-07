from flask import flash, g, Response, jsonify, render_template, redirect, url_for
import application
from application import default, my_jsonify
import datetime
from pandas import DataFrame

def get_appointments():
    data = {}
    conn = application.connect()
    db = conn.cursor(cursor_factory=application.DictCursor)
    # appointments and prescription
    backup = '''with pt(patient_id) as
                (select patient_id
                from patient
                where patient.id = %s)
            select foo.type, d.name, foo.dat, foo.start_time, patient_id, app_id, foo.doc_id, patient_complaint as complaint
            from (((meet natural join pt)
                    natural join doctor_room_slot) 
                    natural join appointment) as foo, (person join doctor on doctor.doc_id=person.id) as d
            where foo.doc_id = d.id
            order by foo.dat desc, foo.start_time desc'''
    sql = '''with pt(patient_id) as
                (select patient_id
                from patient
                where patient.id = %s)
            select foo.type, d.name, foo.instr, foo.dat, foo.start_time, foo.name as medicine, foo.dosage, foo.frequency, patient_id, foo.med_id, app_id, foo.doc_id, patient_complaint as complaint
            from ((((((meet natural join pt)
                    natural join doctor_room_slot) 
                    natural join appointment) 
                    natural left join prescription)
                    natural left join meds)
                    natural left join medicine) as foo, (person join doctor on doctor.doc_id=person.id) as d
            where foo.doc_id = d.id
            order by foo.dat desc, foo.start_time desc'''
            # left outer join medicine on medicine.med_id = meds.med_id) as foo, (person natural join doctor) as d
    db.execute(sql, (g.user.get('id'),))
    rows = db.fetchall()
    if rows != []:  
        df = DataFrame(rows)
        df.columns = rows[0].keys()
        df = df.groupby('app_id', as_index=False).agg({'name':'first', 'dat':'first', 'start_time': 'first', 'complaint': 'first', 'medicine': lambda x: list(x), 'dosage': lambda x: list(x), 'frequency': lambda x: list(x), 'instr': lambda x: list(x)})
        data['appointments'] = df.to_dict(orient='records')
    else:
        data['appointments'] = []
    data['upcoming_appos'] = []
    data['past_appos'] = []
    for appo in data['appointments']:
        appo_time = datetime.datetime.strptime(appo['dat'].isoformat() + ' ' + appo['start_time'].isoformat(), '%Y-%m-%d %H:%M:%S')
        hardcoded_now = datetime.datetime.strptime('2021-05-07 14:00:00', '%Y-%m-%d %H:%M:%S')
        if appo_time >= hardcoded_now: #datetime.datetime.now() + datetime.timedelta(minutes=10)
            data['upcoming_appos'].append(appo)
        else:
            data['past_appos'].append(appo)
    conn.close()
    print(data)
    return render_template('appointments/appointments.html', data=data)

def get_available_slots(date_str):
    data = {}
    if date_str == None:
        date_str = "2021-04-21"
    # date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date
    conn = application.connect()
    db = conn.cursor(cursor_factory=application.DictCursor)
    sql = '''select person.name as name, p.doc_id as id, doctor.speciality, start_time, dat as date
            from doctor natural join
                (
                select doc_id, start_time, dat
                from doctor_room_slot
                except
                select doc_id, start_time, dat
                from meet
                ) as p
                join person on person.id = p.doc_id
            where dat = %s
            '''
    db.execute(sql, (date_str,))
    rows = db.fetchall()
    df = DataFrame(rows)
    if rows == []:
        sql = '''select doctor.id, doctor.name, doctor.speciality 
                from (doctor join person on doc_id=id) as doctor
                '''
        db.execute(sql)
        rows = db.fetchall()
        data['slots'] = [{'name': row['name'], 'id': row['id'], 'speciality': row['speciality'], 'date': date_str, 'start_time': []} for row in rows]
        data['today'] = date_str
        conn.close()
        print(data)
        return render_template('appointments/available_slots.html', data=data)
    df.columns = rows[0].keys()
    df = df.groupby('id', as_index=False).agg({'name':'first', 'speciality':'first', 'date':'first', 'start_time': lambda x: list(x)})
    conn.close()
    data['slots'] = df.to_dict(orient='records')
    data['today'] = date_str
    print(data)
    return render_template('appointments/available_slots.html', data=data) #jsonify(df.to_dict(orient='records'))

def get_available_slots_followup(patient_id, doc_id, date_str):
    data = {}
    if date_str == None:
        date_str = "2021-04-21"
    # date = datetime.datetime.strptime(date_str, '%Y-%m-%d').date
    conn = application.connect()
    db = conn.cursor(cursor_factory=application.DictCursor)
    sql = '''select person.name as name, p.doc_id as id, doctor.speciality, start_time, dat as date
            from doctor natural join
                (
                select doc_id, start_time, dat
                from doctor_room_slot
                except
                select doc_id, start_time, dat
                from meet
                ) as p
                join person on person.id = p.doc_id
            where dat = %s and p.doc_id = %s
            '''
    db.execute(sql, (date_str, doc_id,))
    rows = db.fetchall()
    df = DataFrame(rows)
    if rows == []:
        sql = '''select doctor.id, doctor.name, doctor.speciality 
                from (doctor join person on doc_id=id) as doctor
                where doctor.id = %s
                '''
        db.execute(sql, (doc_id,))
        row = db.fetchone()
        data['slots'] = [{'name': row['name'], 'id': doc_id, 'speciality': row['speciality'], 'date': date_str, 'start_time': []}]
        data['today'] = date_str
        data['patient_id'] = patient_id
        conn.close()
        return render_template('appointments/follow_up.html', data=data)
    df.columns = rows[0].keys()
    df = df.groupby('id', as_index=False).agg({'name':'first', 'speciality':'first', 'date':'first', 'start_time': lambda x: list(x)})
    conn.close()
    data['slots'] = df.to_dict(orient='records')
    data['today'] = date_str
    data['patient_id'] = patient_id
    print(data)
    return render_template('appointments/follow_up.html', data=data) #jsonify(df.to_dict(orient='records'))

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
        flash('Failed to book appointment!', 'danger')
        return redirect(url_for('get_appointments'))    
    flash('Apoointment booked successfully!', 'success')
    return redirect(url_for('get_appointments')) #render_template('appointments/appointments.html') #jsonify({'status':'Successfully booked a new appointment', 'code':200})

def update_complaint(request):
    app_id = int(request.get('app_id'))
    patient_id = int(request.get('patient_id'))
    complaint = request.get('complaint')
    conn = application.connect()
    db = conn.cursor(cursor_factory=application.DictCursor)
    try:
        sql = '''update meet
                set patient_complaint = %s
                where app_id = %s and patient_id = %s returning *;
                '''
        db.execute(sql, (complaint, app_id, patient_id,))
        update_meet = db.fetchone()
        if update_meet is None:
            raise Exception('no appointment updated')
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)
        conn.rollback()
        conn.close()
        flash('Failed to update appointment!', 'danger')
        return redirect(url_for('get_appointments'))    
    flash('Appointment updated successfully!', 'success')
    return redirect(url_for('get_appointments'))

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
        flash('Failed to cancel appointment!', 'danger')
        return redirect(url_for('get_appointments'))    
    flash('Apoointment cancelled successfully!', 'success')
    return redirect(url_for('get_appointments'))