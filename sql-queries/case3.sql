--view/modify personal info
--1) view personal details--------------------------------------
select *
from person as p
where p.id = 10; --fill correct one

--2) update basic details----------------------------------------
update person
set (name,address,pincode,contact) = ('Binod','IITB',400096,'1234567890')
where id = 10;

--2.5) add disease history---------------------------------------
select disease_id
from disease
where name = 'Flu'

insert into history
values (10,12,'this.com','2020-03-15')

--3) past appointments---------------------------------------------
with pt(patient_id) as
	(select patient_id
	from patient
	where id = 1) --fill correct one
select foo.type, p.name, foo.instr, foo.dat, foo.start_time
from ((((meet natural join pt)
		natural join doctor_room_slot) 
		natural join appointment) 
		natural join prescription) as foo, person as p
where foo.doc_id = p.id

--4) future appointments--------------------------------------------
with pt(patient_id) as
	(select patient_id
	from patient
	where id = 1) --fill correct one
select foo.type, p.name, foo.dat, foo.start_time
from (((meet natural join pt)
		natural join doctor_room_slot)
		natural join appointment) as foo, person as p
where foo.doc_id = p.id and foo.dat >= date(now())

--5) bill status-----------------------------------------------------
with pt(patient_id) as
	(select patient_id
	from patient
	where person.id = 10) --fill correct one
((select opd_charges, purpose, discount, (case when person_id is null then 'unpaid' else 'paid')
from ((((meet natural join pt)
		natural join appointment)
		natural join bill_no)
		natural join doctor) as foo)
union
(select charges,purpose,discount, (case when person_id is null then 'unpaid' else 'paid')
from (((pt natural join takes)
		natural join bill)
		natural join test) as bar))
union
(select charges*(end_dt-start_dt), purpose, discount, (case when person_id is null then 'unpaid' else 'paid')
from (((pt natural join occupies)
		natural join bill)
		natural join bed)
as foo) 

--6) event??

--7) admitted--------------------------------------------------------
with pt(patient_id) as
	(select patient_id
	from patient
	where id = 2) --fill correct one
select foo.disease_name, foo.start_dt, foo.end_dt
from ((((meet natural join pt)
		natural join occupies)
		natural join suffers)
		natural join disease) as foo

--8) disease hist-----------------------------------------------------
with pt(patient_id) as 
	(select patient_id
	from patient
	where id = 2) --fill correct one
select disease_name, min(detected)
from	((select disease_name, detected
		from history natural join disease
		where person_id = 2)
		union
		(select disease_name, min(dat) as detected
		from (select disease_name, dat
				from (((suffers natural join pt)
					natural join disease)
					natural join meet) as foo) as bar
		group by disease_name)) as foo
group by disease_name