--bill generation

--1) Appointment fees
insert into bill
values(10,12,'Appointment for regular check-up',0,'online') --paid bill

insert into bill
values(10,NULL,'Appointment for regular check-up',0,NULL) --unpaid bill

update appointment
set bill_no = 10
where app_id = 12

--2) Bill for test
insert into bill
values(10,12,'Blood_test',20,'online') --paid bill

update takes
set bill_no = 10
where patient_id = 12 and test_id = 1 and dat = 2021-20-03

--3) Bill for medicine
insert into bill
values(10,12,'Medicines',20,'Cash')

insert into bill_med
values(10,1,2)

--To show the medicines for the bill
select name, qty, price*qty
from (select med_id, qty
	from bill_med
	where bill_no = 10) as foo natural join medicine

--4) Bill for admitted patient
insert into bill
values (10,NULL,'Bed_charges',10,NULL)

update occupies
set bill_no = 10
where patient_id = 12
