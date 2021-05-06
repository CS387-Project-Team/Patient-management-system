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

    #doctor role
    db.execute('select * from doctor where doc_id = %s', (g.user.get('id'),))
    row = db.fetchone()
    if row is not None:
        data['doctor'] = True
    else:
        data['doctor'] = False
    
    #staff role
    db.execute('select * from support_staff where staff_id = %s',(g.user.get('id'),))
    row = db.fetchone()
    if row is not None:
        data['staff'] = True
    else:
        data['staff'] = False

    #admin role
    db.execute('select * from admin where id = %s',(g.user.get('id'),))
    row = db.fetchone()
    if row is not None:
        data['admin'] = True
    else:
        data['admin'] = False
    
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

    # user analytics
    ## cost split
    data['expenses'] = {}
    sql = '''select  coalesce(sum(opd_charges),0) as opd_charges
            from person natural join patient natural join meet natural join doctor
            where person.id = %s
            '''
    db.execute(sql, (id,))
    data['expenses']['doctor'] = db.fetchone()['opd_charges']
    sql = '''select  coalesce(sum(charges),0) as test_charges
            from person natural join patient natural join takes natural join test
            where person.id = %s
            '''
    db.execute(sql, (id,))
    data['expenses']['test'] = db.fetchone()['test_charges']
    sql = '''select  coalesce(sum(qty*price),0) as med_charges
            from person natural join bill natural join bill_med natural join medicine
            where person.id = %s
            '''
    db.execute(sql, (id,))
    data['expenses']['meds'] = db.fetchone()['med_charges']
    sql = '''select coalesce(sum((end_dt-start_dt)*charges),0) as bed_charges
            from person natural join patient natural join occupies natural join bed
            where person.id = %s
            '''
    db.execute(sql, (id,))
    data['expenses']['bed'] = db.fetchone()['bed_charges']

    ## top 5 diseases suffered by person
    sql = '''select disease_name as name, count(*) as freq
            from person natural join patient natural join suffers natural join disease
            where person.id = %s
            group by disease_name
            order by freq desc;
            '''
    db.execute(sql, (id,))
    top_diseases = db.fetchall()
    total = 0
    data['top_diseases'] = []
    for s in top_diseases:
        total += s['freq']
    
    iter_ = 0
    perc_cum = 0
    for s in top_diseases:
        iter_ += 1
        cur_disease = {}
        cur_disease['name'] = s['name']
        cur_disease['perc'] = s['freq'] / total * 100
        perc_cum += cur_disease['perc']
        if iter_ == application.MAX_NUM_DISEASES + 1:
            cur_disease['name'] = 'Others'
            cur_disease['perc'] = 100 - perc_cum
        
        data['top_diseases'].append(cur_disease)
    if top_diseases == []:
        dummy = {}
        dummy['name'] = 'Others'
        dummy['perc'] = 100
        data['top_diseases'].append(dummy)
    conn.close()
    
    total_expenses = sum(data['expenses'].values())
    if total_expenses != 0:
        for k in data['expenses'].keys():
            data['expenses'][k] *= 100 / total_expenses
    data['expenses']['total'] = total_expenses
    print(data['expenses'])
    print(data['top_diseases'])
    return render_template('dashboard/dashboard.html', data=data) #jsonify(data)

def view_history():
    data = {}

    conn = application.connect()
    db = conn.cursor(cursor_factory=application.DictCursor)
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
            '''
    id = g.user.get('id')
    db.execute(sql, (id,id,))
    rows = db.fetchall()
    data['history'] = my_jsonify(rows)
    conn.close()
    return render_template('history/view_history.html', data=data)

def get_history_for_edit():
    data = {}
    conn = application.connect()
    db = conn.cursor(cursor_factory=application.DictCursor)
    # history
    sql = '''select disease_name as name, prev_hist_link as link, detected
                from history natural join disease
                where person_id = %s
                order by detected desc
        '''
    id = g.user.get('id')
    db.execute(sql, (id,))
    rows = db.fetchall()
    data['history'] = my_jsonify(rows)
    sql = '''select disease_name from disease'''
    db.execute(sql)
    rows = db.fetchall()
    data['diseases'] = my_jsonify(rows)
    return render_template('history/edit_history.html', data=data)

def add_history(data):
    dis_det_link_data = zip(data.getlist('disease[]'), data.getlist('detected[]'), data.getlist('hist_link[]'))
    select = '''select disease_id from disease
                where disease_name = %s
            '''
    insert = '''insert into history(person_id, disease_id, prev_hist_link, detected)
            values (%s, %s, %s, %s)
        '''
    conn = application.connect()
    db = conn.cursor(cursor_factory=application.DictCursor)
    for (disease,detected,link) in dis_det_link_data:
        try:
            row = db.execute(select, (disease,))
            row = db.fetchone()
            disease_id = row['disease_id']
            db.execute(insert, (g.user.get('id'), disease_id, link, detected))
            conn.commit()
        except Exception as e:
            print(e)
            conn.rollback()
    conn.close()
    return redirect(url_for('add_history'))

def delete_history(data):
    print(data)
    conn = application.connect()
    disease_name = data['disease_name']
    link = data['link']
    detected = data['detected']
    db = conn.cursor(cursor_factory=application.DictCursor)
    try:
        sql = '''select disease_id from disease
                where disease_name = %s
                '''
        db.execute(sql, (disease_name,))
        row = db.fetchone()
        disease_id = row['disease_id']
        sql = '''delete from history
                where person_id = %s and disease_id = %s returning *;
                '''
        db.execute(sql, (g.user.get('id'), disease_id))
        row = db.fetchone()
        if row is None:
            raise('no row was deleted')
        conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()
    conn.close()
    return redirect(url_for('add_history'))

def update_history(data):
    print(data)
    conn = application.connect()
    disease_name = data['disease_name']
    link = data['link']
    detected = data['detected']
    old_disease_name = data['old_disease_name']
    db = conn.cursor(cursor_factory=application.DictCursor)
    try:
        sql = '''select disease_id from disease
                where disease_name = %s
                '''
        db.execute(sql, (old_disease_name,))
        row = db.fetchone()
        old_disease_id = row['disease_id']
        sql = '''select disease_id from disease
                where disease_name = %s
                '''
        db.execute(sql, (disease_name,))
        row = db.fetchone()
        disease_id = row['disease_id']
        sql = '''update history
                set disease_id = %s, detected = %s, prev_hist_link = %s
                where disease_id = %s and person_id = %s;
                '''
        db.execute(sql, (disease_id, detected, link, old_disease_id, g.user.get('id'),))
        conn.commit()
    except Exception as e:
        print(e)
        conn.rollback()
    conn.close()
    return redirect(url_for('add_history'))