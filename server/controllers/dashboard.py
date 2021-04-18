from flask import g, Response, jsonify
import application
from application import default, my_jsonify
import datetime
   
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
            select foo.type, d.name, foo.instr, foo.dat, foo.start_time, foo.name as medicine, foo.dosage, foo.frequency
            from ((((((meet natural join pt)
                    natural join doctor_room_slot) 
                    natural join appointment) 
                    natural join prescription)
                    natural join meds)
                    natural join medicine) as foo, (person natural join doctor) as d
            where foo.doc_id = d.id'''
    db.execute(sql, (g.user.get('id'),))
    rows = db.fetchall()
    data['appointments'] = my_jsonify(rows)
    
    # bills
    sql = '''with pt(patient_id) as
                (select patient_id
                from patient
                where patient.id = %s)
            (select opd_charges, purpose, discount, (case when paid_by is null then 'unpaid' else 'paid' end)
            from ((((meet natural join pt)
                    natural join appointment)
                    natural join bill)
                    natural join doctor) as foo)
            union
            (select charges,purpose,discount, (case when paid_by is null then 'unpaid' else 'paid' end)
            from (((pt natural join takes)
                    natural join bill)
                    natural join test) as bar)
            union
            (select charges*(end_dt-start_dt), purpose, discount, (case when paid_by is null then 'unpaid' else 'paid' end)
            from (((pt natural join occupies)
                    natural join bill)
                    natural join bed) as foo)'''
    db.execute(sql, (g.user.get('id'),))
    rows = db.fetchall()
    data['bills'] = my_jsonify(rows)

    # tests
    sql = '''with pt(patient_id) as
                (select patient_id
                from patient
                where patient.id = %s)
            select name as test, result_file , comments, dat
            from (takes natural join pt natural join test) as foo'''
    db.execute(sql, (g.user.get('id'),))
    rows = db.fetchall()
    data['tests'] = my_jsonify(rows)

    # history
    sql = '''with pt(patient_id) as 
                (select patient_id
                from patient
                where patient.id = %s),
                foo(name, detected) as 
                (select name, detected
                from ((history natural join pt)
                        natural join disease)
                where person_id = %s)
            (select name, min(dat) as detected
            from (select name, dat
                    from (((suffers natural join pt)
                        natural join disease)
                        natural join meet) as bar
                    where not exists(select 1 from foo
                                    where foo.name = bar.name)) as bar group by name)
            union
            select * from foo'''
    id = g.user.get('id')
    db.execute(sql, (id,id,))
    rows = db.fetchall()
    data['history'] = my_jsonify(rows)

    conn.close()
    return jsonify(data)