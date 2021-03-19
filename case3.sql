--view/modify personal info
--1) view personal details
select *
from person as p
where p.id = 10; --fill correct one

--2) update basic details
update person
set (name,address,pincode,contact) = ('Binod','IITB',400096,'1234567890')
where id = 10;

--3) past appointments
with pt(patient_id) as
	(select patient_id
	from patient
	where person.id = 10) --fill correct one
select foo.app_type, d.doc_name, foo.instr, foo.dat, foo.start_time
from ((((((meet natural join pt)
		natural join doctor_room_slot) 
		natural join appointment) 
		natural join prescribes)
		natural join prescription) as foo, doctor as d
where foo.doc_id = d.id

--4) future appointments
with pt(patient_id) as
	(select patient_id
	from patient
	where person.id = 10) --fill correct one
select foo.app_type, d.doc_name, foo.dat, foo.start_time
from ((meet natural join pt)
		natural join doctor_room_slot) as foo, doctor as doctor_room_slot
where foo.doc_id = d.id and foo.dat > 2021-19-03

--5) bill status
select foo.paid, 

--6) event??

--7) admitted

--8) disease hist