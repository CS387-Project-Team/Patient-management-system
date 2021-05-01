from flask import g, Response, jsonify, render_template, redirect, url_for
import application
from application import default, my_jsonify
import datetime


def get_profile():
    data = {}

    # user profile
    conn = application.connect()
    db = conn.cursor(cursor_factory=application.DictCursor)
    db.execute('select * from person where id = %s', (g.user.get('id'),))
    row = db.fetchone()
    data['user'] = my_jsonify(row, multiple=False)

    conn.close()
    print(data['user'])
    return render_template('dashboard/profile.html', data=data)

def update_profile(request):
    # user profile
    conn = application.connect()
    db = conn.cursor(cursor_factory=application.DictCursor)
    try:
        sql = '''update person
                set (name, username, address, pincode, contact, gender, email_id, dob) = (%s, %s, %s, %s, %s, %s, %s)
                where id = %s;
                '''
        db.execute(sql, (request.get('name'), request.get('username'), request.get('address'), request.get('pincode'), request.get('contact'), request.get('gender'), request.get('email_id'), request.get('dob'), g.user.get('id'),))
    except Exception as e:
        print(e)
        conn.rollback()
        conn.close()
        redirect(url_for('profile'))
    
    conn.commit()
    conn.close()
    return redirect(url_for('profile'))

def get_dashboard():
    data = {}

    # user profile
    conn = application.connect()
    db = conn.cursor(cursor_factory=application.DictCursor)
    db.execute('select * from person where id = %s', (g.user.get('id'),))
    row = db.fetchone()
    data['user'] = my_jsonify(row, multiple=False)
    
    # appointments and prescription
    sql = '''with pt(patient_id) as
                (select patient_id
                from patient
                where patient.id = %s)
            select foo.type, d.name, foo.instr, foo.dat, foo.start_time, foo.name as medicine, foo.dosage, foo.frequency, patient_id, med_id, app_id, foo.doc_id, patient_complaint as complaint
            from ((((((meet natural join pt)
                    natural join doctor_room_slot) 
                    natural join appointment) 
                    natural left join prescription)
                    natural left join meds)
                    natural left outer join medicine) as foo, (person join doctor on doctor.doc_id=person.id) as d
            where foo.doc_id = d.doc_id
            order by foo.dat desc
            limit 3'''
        #     left outer join medicine on medicine.med_id = meds.med_id) as foo, (person natural join doctor) as d
    db.execute(sql, (g.user.get('id'),))
    rows = db.fetchall()
    data['appointments'] = my_jsonify(rows)
    
    # bills
    sql = '''with pt(patient_id) as
                (select patient_id
                from patient
                where patient.id = %s)
            select * 
            from
            (
                (select opd_charges as net_charges, purpose, discount, (case when paid_by is null then 'unpaid' else 'paid' end) as status, dat
                from ((((meet natural join pt)
                        natural join appointment)
                        natural join bill)
                        natural join doctor) as foo)
                union
                (select charges  as net_charges, purpose, discount, (case when paid_by is null then 'unpaid' else 'paid' end) as status, dat
                from (((pt natural join takes)
                        natural join bill)
                        natural join test) as bar)
                union
                (select charges*(end_dt-start_dt) as net_charges, purpose, discount, (case when paid_by is null then 'unpaid' else 'paid' end) as status, start_dt as dat
                from (((pt natural join occupies)
                        natural join bill)
                        natural join bed) as foo)
            ) as foo
            order by status desc, dat desc
            limit 3'''
    db.execute(sql, (g.user.get('id'),))
    rows = db.fetchall()
    data['bills'] = my_jsonify(rows)

    # tests
    sql = '''with pt(patient_id) as
                (select patient_id
                from patient
                where patient.id = %s)
            select name as test, result_file , comments, dat
            from (takes natural join pt natural join test) as foo
            '''
    db.execute(sql, (g.user.get('id'),))
    rows = db.fetchall()
    data['tests'] = my_jsonify(rows)

    # history
    sql = '''with pt(patient_id) as 
                (select patient_id
                from patient
                where patient.id = %s),
                foo(name, detected) as 
                (select disease_name, detected
                from ((history natural join pt)
                        natural join disease)
                where person_id = %s)
            select * 
            from
            (
                (select name, min(dat) as detected
                from (select disease_name as name, dat
                        from (((suffers natural join pt)
                                natural join disease)
                                natural join meet) as bar
                        where not exists(select 1 from foo
                                        where foo.name = bar.disease_name)) as bar group by name)
                union
                select * from foo
            ) as foo
            order by detected desc
            limit 3'''
    id = g.user.get('id')
    db.execute(sql, (id,id,))
    rows = db.fetchall()
    data['history'] = my_jsonify(rows)

    conn.close()
    print(data['appointments'])
    return render_template('dashboard/dashboard.html', data=data) #jsonify(data)