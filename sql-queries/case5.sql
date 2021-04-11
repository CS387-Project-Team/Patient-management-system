-- Show free slots from case4.sql

-- Book a followup
-- inputs app_id, patient_id, book_doc_id, book_date, book_time, appo_type

begin;
    insert into appointment(app_id, type)
    values app_id, appo_type;
    insert into meet(app_id, patient_id, doc_id, room_no, dat, start_time, patient_complaint)
    values app_id, patient_id, book_doc_id, book_date, book_time, complaint;
commit;

-- Cancel a followup
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
commit;