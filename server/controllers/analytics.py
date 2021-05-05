from flask import g, Response, jsonify, render_template, redirect, url_for
import application
from application import default, my_jsonify
import datetime

def get_analytics(json_=True):
    data = {}
    # data about bed occupancy vs date
    cur_date = datetime.datetime.strptime('2021-01-01', '%Y-%m-%d').date() # hardcoded for now
    print(cur_date)
    conn = application.connect()
    db = conn.cursor(cursor_factory=application.DictCursor)
    sql = '''select start_dt, count(*) as admissions from occupies
            group by start_dt
            order by start_dt'''
    db.execute(sql)
    admissions = db.fetchall()
    sql = '''select end_dt, count(*) as discharges from occupies
            where end_dt is not null
            group by end_dt
            order by end_dt'''
    db.execute(sql)
    discharges = db.fetchall()

    sql = '''select dat, count(*) as appos from meet
            where dat is not null
            group by dat
            order by dat'''
    db.execute(sql)
    appos = db.fetchall()

    sql = '''select count(*) as beds from bed
            '''
    db.execute(sql)
    total_beds = db.fetchone()
    data['daywise'] = []
    data['total_beds'] = total_beds['beds']
    occupied = 0
    admit_iter = 0
    discharge_iter = 0
    appo_iter = 0
    while True:
        daywise = {}
        daywise['date'] = cur_date.isoformat()
        if admit_iter >= len(admissions) or cur_date < admissions[admit_iter]['start_dt']:
            daywise['admissions'] = 0
        else:
            daywise['admissions'] = admissions[admit_iter]['admissions']
            admit_iter += 1
        if discharge_iter >= len(discharges) or cur_date < discharges[discharge_iter]['end_dt']:
            daywise['discharges'] = 0
        else:
            daywise['discharges'] = discharges[discharge_iter]['discharges']
            discharge_iter += 1
        if appo_iter >= len(appos) or cur_date < appos[appo_iter]['dat']:
            daywise['appos'] = 0
        else:
            daywise['appos'] = appos[appo_iter]['appos']
            appo_iter += 1
        occupied = occupied + daywise['admissions'] - daywise['discharges']
        daywise['occupied'] = occupied

        data['admits'] = daywise['admissions']
        data['discharges'] = daywise['discharges']
        data['daywise'].append(daywise)
        cur_date += datetime.timedelta(days=1)
        if cur_date >= datetime.date.today():
            break
    data['occupied'] = occupied
    
    # top k areas/specialities
    k = 5
    sql = '''select speciality, count(*) as freq
            from meet natural join doctor
            group by speciality
            order by freq desc
            '''
    db.execute(sql)
    top_areas = db.fetchall()
    top_areas = get_top_k(top_areas, k, key1='speciality', key2='freq')

    # top k doctors
    sql = '''select person.name as name, count(*) as freq
            from (meet inner join doctor on doctor.doc_id=meet.doc_id) inner join person on doctor.doc_id=person.id
            group by person.id, person.name
            order by freq desc
            '''
    db.execute(sql)
    top_docs = db.fetchall()
    top_docs = get_top_k(top_docs, k, key1='name', key2='freq')

    # top k tests
    sql = '''select test.name as name, count(*) as freq
            from takes natural join test
            group by test_id, test.name
            order by freq desc
            '''
    db.execute(sql)
    top_tests = db.fetchall()
    top_tests = get_top_k(top_tests, k, key1='name', key2='freq')

    # top k diseases
    sql = '''select disease_name, count(*) as freq
            from meet natural join suffers natural join disease
            group by doc_id, disease_name
            order by freq desc
            '''
    db.execute(sql)
    top_diseases = db.fetchall()
    top_diseases = get_top_k(top_diseases, k, key1='disease_name', key2='freq')

    # top k medicines
    sql = '''select medicine.name as name, sum(qty) as qty
            from bill_med natural join medicine
            group by med_id, medicine.name
            order by qty desc
            '''
    db.execute(sql)
    top_meds = db.fetchall()
    top_meds = get_top_k(top_meds, k, key1='name', key2='qty')
    conn.close()
    data['top_areas'] = top_areas
    data['top_docs'] = top_docs
    data['top_diseases'] = top_diseases
    data['top_meds'] = top_meds
    data['top_tests'] = top_tests
    if json_:
        return jsonify(data)
    return data


def get_disease_analytics(disease_id):
    data = {}
    # data about disease and symptoms
    conn = application.connect()
    db = conn.cursor(cursor_factory=application.DictCursor)
    sql = '''select symp_name, count(*) as frac
            from symptom natural join shows natural join meet natural join patient natural join suffers natural join disease
            where disease_id = %s
            group by symp_name
            order by frac desc; 
            '''
    db.execute(sql, (disease_id,))
    symptoms = db.fetchall()
    total = 0
    data['symptoms'] = []
    for s in symptoms:
        total += s['frac']
    
    iter_ = 0
    perc_cum = 0
    for s in symptoms:
        iter_ += 1
        cur_symptom = {}
        cur_symptom['name'] = s['symp_name']
        cur_symptom['perc'] = s['frac'] / total * 100
        perc_cum += cur_symptom['perc']
        if iter_ == 10:
            cur_symptom['name'] = 'Others'
            cur_symptom['perc'] = 100 - perc_cum
        
        data['symptoms'].append(cur_symptom)
    if symptoms == []:
        dummy = {}
        dummy['name'] = 'Others'
        dummy['perc'] = 100
        data['symptoms'].append(dummy)

    # data about disease and medicines
    sql = '''select medicine.name as med_name, count(*) as frac
            from medicine natural join meds natural join prescription natural join appointment natural join meet natural join patient natural join suffers natural join disease
            where disease_id = %s
            group by med_name
            order by frac desc; 
            '''
    db.execute(sql, (disease_id,))
    medicines = db.fetchall()
    total = 0
    data['medicines'] = []
    for s in medicines:
        total += s['frac']
    
    iter_ = 0
    perc_cum = 0
    for s in medicines:
        iter_ += 1
        cur_medicine = {}
        cur_medicine['name'] = s['med_name']
        cur_medicine['perc'] = s['frac'] / total * 100
        perc_cum += cur_medicine['perc']
        if iter_ == 10:
            cur_medicine['name'] = 'Others'
            cur_medicine['perc'] = 100 - perc_cum
        
        data['medicines'].append(cur_medicine)
    if medicines == []:
        dummy = {}
        dummy['name'] = 'Others'
        dummy['perc'] = 100
        data['medicines'].append(dummy)
    
    conn.close()

    daily_trends = get_disease_daily_trends(disease_id)
    data['daywise'] = daily_trends['daywise']
    data['total_beds'] = daily_trends['total_beds']
    return jsonify(data)

def get_top_k(rows, k, key1='name', key2='freq'):
    iter_ = 0
    ret_list = []
    perc_cum = 0
    total = 0
    for row in rows:
        total += row[key2]

    if total == 0:
        return []
    
    for row in rows:
        iter_ += 1
        cur_dict = {}
        cur_dict['label'] = row[key1]
        cur_dict['y'] = round(row[key2] / total * 100, 2)
        perc_cum += cur_dict['y']
        ret_list.append(cur_dict)
        if iter_ == k:
            cur_dict['label'] = 'Others'
            cur_dict['y'] = 100 - perc_cum
    return ret_list
    
def get_disease_daily_trends(disease_id):
    # data about bed occupancy vs date
    cur_date = datetime.datetime.strptime('2021-01-01', '%Y-%m-%d').date() # hardcoded for now
    print(cur_date)
    conn = application.connect()
    db = conn.cursor(cursor_factory=application.DictCursor)
    sql = '''select start_dt, count(*) as admissions 
            from occupies natural join patient natural join suffers natural join disease
            where disease_id = %s
            group by start_dt
            order by start_dt'''
    db.execute(sql, (disease_id,))
    admissions = db.fetchall()
    sql = '''select end_dt, count(*) as discharges 
            from occupies natural join patient natural join suffers natural join disease
            where end_dt is not null and disease_id = %s
            group by end_dt
            order by end_dt'''
    db.execute(sql, (disease_id,))
    discharges = db.fetchall()

    sql = '''select dat, count(*) as appos 
            from meet natural join patient natural join suffers natural join disease
            where dat is not null and disease_id = %s
            group by dat
            order by dat'''
    db.execute(sql, (disease_id,))
    appos = db.fetchall()

    sql = '''select count(*) as beds from bed
            '''
    db.execute(sql)
    total_beds = db.fetchone()
    conn.close()
    return convert_analytics_data(total_beds, appos, discharges, admissions, cur_date)

def convert_analytics_data(total_beds, appos, discharges, admissions, cur_date):
    data = {}
    data['daywise'] = []
    data['total_beds'] = total_beds['beds']
    occupied = 0
    admit_iter = 0
    discharge_iter = 0
    appo_iter = 0
    while True:
        daywise = {}
        daywise['date'] = cur_date.isoformat()
        if admit_iter >= len(admissions) or cur_date < admissions[admit_iter]['start_dt']:
            daywise['admissions'] = 0
        else:
            daywise['admissions'] = admissions[admit_iter]['admissions']
            admit_iter += 1
        if discharge_iter >= len(discharges) or cur_date < discharges[discharge_iter]['end_dt']:
            daywise['discharges'] = 0
        else:
            daywise['discharges'] = discharges[discharge_iter]['discharges']
            discharge_iter += 1
        if appo_iter >= len(appos) or cur_date < appos[appo_iter]['dat']:
            daywise['appos'] = 0
        else:
            daywise['appos'] = appos[appo_iter]['appos']
            appo_iter += 1
        occupied = occupied + daywise['admissions'] - daywise['discharges']
        daywise['occupied'] = occupied

        data['daywise'].append(daywise)
        cur_date += datetime.timedelta(days=1)
        if cur_date >= datetime.date.today():
            break
    
    return data

def show_disease_analytics(disease_id):
    data = {}
    data['disease_id'] = disease_id
    # data about all disease names
    conn = application.connect()
    db = conn.cursor(cursor_factory=application.DictCursor)
    sql = '''select disease_name from disease; 
            '''
    db.execute(sql)
    diseases = db.fetchall()
    data['diseases'] = my_jsonify(diseases)
    db = conn.cursor(cursor_factory=application.DictCursor)
    sql = '''select disease_name from disease where disease_id=%s; 
            '''
    db.execute(sql, (disease_id,))
    row = db.fetchone()
    data['disease_name'] = row['disease_name']
    conn.close()
    return render_template('analytics/disease-wise.html', data=data)

def post_disease_for_analytics(disease_name):
    conn = application.connect()
    db = conn.cursor(cursor_factory=application.DictCursor)
    sql = '''select disease_id from disease where disease_name = %s; 
            '''
    db.execute(sql, (disease_name,))
    diseases = db.fetchone()
    disease_id = diseases['disease_id']
    conn.close()
    return redirect(url_for('show_disease_analytics', disease_id=disease_id)) #render_template('analytics/disease-wise.html', data=data)