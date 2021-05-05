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

def get_available_tests():
    conn = application.connect()
    db = conn.cursor(cursor_factory=application.DictCursor)
    sql='''SELECT test_id, name, charges from test'''
    db.execute(sql)
    rows = db.fetchall()
    if rows == []:
        return jsonify({'msg':'No data found'})

    data={}
    data['available_tests']=[]
    for r in rows:
        data['available_tests'].append({"id":r[0], "name":r[1],"charge":float(r[2])})
    print(data)
    return render_template('tests/available_tests.html', data=data)

def confirm_booking(request):
    data = {}
    data['doctor_name'] = request.get('doctor_name')
    data['doctor_id'] = int(request.get('doctor_id'))
    data['date'] = request.get('date')
    data['time'] = request.get('time')
    return render_template('appointments/confirm_booking.html', data=data)

def book_test(request):
    print(request)
    test_id = int(request.get('test_id'))
    date = request.get('date')
    print(request)
    user_id = g.user['id']
    conn = application.connect()
    db = conn.cursor(cursor_factory=application.DictCursor)
    try:
        sql = '''SELECT 1+max(patient_id) as new_id
                        from patient'''
        db.execute(sql)
        row = db.fetchone()
        patient_id = row['new_id']
        sql = '''INSERT into patient(id, patient_id)
                values (%s, %s);'''
        db.execute(sql, (user_id, patient_id,))

        sql='''INSERT into takes(patient_id, test_id, dat)
                values(%s,%s,%s);'''
        db.execute(sql,(patient_id, test_id,date))

        conn.commit()
        conn.close()
    except Exception as e:
        print(e)
        conn.rollback()
        conn.close()
        return jsonify({'status':'Failed to book a new test', 'code':401})    
    flash('Diagnostic test booked successfully!', 'success')
    return redirect(url_for('get_tests'))


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