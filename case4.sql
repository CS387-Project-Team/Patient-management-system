-- Show free slots
-- inputs book_doc_id, book_date

select start_time from slot
where dat = book_date 
except
select start_time from meet
where doctor_id = book_doc_id and dat = book_date;

-- Book an appointment
-- inputs app_id, person_id, patient_id, book_doc_id, book_date, book_time, appo_type

-- prepare create_appo (text) as
--     insert into appointment(type) values($1);
-- prepare add_meet () as
--     insert into meet(patient_id, doc_id, dat, start_time, patient_complaint)
begin;
    insert into patient(id, patient_id)
    values person_id, patient_id;
    insert into appointment(app_id, type)
    values app_id, appo_type;
    insert into meet(app_id, patient_id, doc_id, room_no, dat, start_time, patient_complaint)
    values app_id, patient_id, book_doc_id, book_date, book_time, complaint;
commit;

-- Cancel an appointment
-- inputs patient_id, book_doc_id, book_date, book_time
begin;
    with app as (
        select app_id from meet
        where patient_id = patient_id and doctor_id = book_doc_id and dat = book_date and start_time = book_time
    )
    delete from appointment
    where app_id = (select app.app_id from app); 
    delete from meet
    where patient_id = patient_id and doctor_id = book_doc_id and dat = book_date, start_time = book_time;
    delete from patient
    where patient_id = patient_id;
commit;