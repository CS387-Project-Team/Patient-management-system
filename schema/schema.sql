drop table if exists visits;
drop table if exists assg_to;
drop table if exists meds;
drop table if exists occupies;
drop table if exists bill_med;
drop table if exists should_take;
drop table if exists takes;
drop table if exists shows;
drop table if exists suffers;
drop table if exists history;
drop table if exists meet;
drop table if exists handle;
drop table if exists doctor_room_slot;
drop table if exists medicine;
drop table if exists equipment;
drop table if exists test;
drop table if exists bed;
drop table if exists disease;
drop table if exists symptom;
drop table if exists appointment;
drop table if exists bill;
drop table if exists prescription;
drop table if exists room;
drop table if exists slot;
drop table if exists patient;
drop table if exists admin;
drop table if exists support_staff;
drop table if exists doctor;
drop table if exists person;


CREATE EXTENSION IF NOT EXISTS pgcrypto;

create table person
	(id int,
	name text not NULL,
	address text,
	pincode int,
	contact varchar(10),
	gender varchar(2)
		check (gender in ('M','F',NULL)),

	username text,
	password text,
	email_id text
		check (email_id like '%@%'),
	dob date,
		--check (dob <= date(now())),
	qualification text,
	primary key(id)
	);

-- insert into person values(0,'Admin','IITB',123456,1234567890,'M','Ramu','Ramu','foo@gmail.com','2000-01-01','Btech');
-- insert into person values(1,'P0','IITB',123456,1234567890,'M','Ramu','Ramu','foo@gmail.com','2000-01-01','Btech');
-- insert into person values(2,'P1','IITB',123456,1234567890,'M','Ramu','Ramu','foo@gmail.com','2000-01-01','Btech');
-- insert into person values(3,'P2','IITB',123456,1234567890,'M','Ramu','Ramu','foo@gmail.com','2000-01-01','Btech');
-- insert into person values(4,'D1','IITB',123456,1234567890,'M','Ramu','Ramu','foo@gmail.com','2000-01-01','Btech');
-- insert into person values(5,'D2','IITB',123456,1234567890,'M','Ramu','Ramu','foo@gmail.com','2000-01-01','Btech');
-- insert into person values(6,'S1','IITB',123456,1234567890,'M','Ramu','Ramu','foo@gmail.com','2000-01-01','Btech');
-- insert into person values(7,'S2','IITB',123456,1234567890,'M','Ramu','Ramu','foo@gmail.com','2000-01-01','Btech');
-- insert into person values(8,'S3','IITB',123456,1234567890,'M','Ramu','Ramu','foo@gmail.com','2000-01-01','Btech');
-- insert into person values(9,'S4','IITB',123456,1234567890,'M','Ramu','Ramu','foo@gmail.com','2000-01-01','Btech');

create table doctor
	(doc_id int,
	speciality text,
		--check (speciality in ("Physician","Cardiology","Nephrology","Orthopaedic","Skin","Neurology")),
	-- qualification text,
	salary int
		check(salary > 0),
	permanent boolean,
	experience int,
	opd_charges int,
	ot_charges int,
	primary key (doc_id),
	foreign key (doc_id) references person
		on delete cascade
	);

-- insert into doctor values(4,'Phys',22222,NULL,10,200,2000);
-- insert into doctor values(5,'Card',22222,NULL,10,200,2000);

create table support_staff
	(staff_id int,
	role text,
	-- qualification text,
	experience int,
	salary int
		check(salary > 0),
	start_hr int,
	end_hr int,
	days_of_week text,
	primary key (staff_id),
	foreign key (staff_id) references person
		on delete cascade
	);

-- insert into support_staff values(6,'Nursing',10,10000,8,14,'Mon-Fri');
-- insert into support_staff values(7,'Nursing',10,10000,8,14,'Mon-Fri');
-- insert into support_staff values(8,'Equipment',10,10000,8,14,'Mon-Fri');
-- insert into support_staff values(9,'Equipment',10,10000,8,14,'Mon-Fri');

create table admin
	(id int,
	salary int
		check(salary > 0),
	-- qualification text,
	primary key (id),
	foreign key (id) references person
		on delete cascade
	);
-- insert into admin values(0,1000000);

create table patient
	(id int,
	patient_id int,
	primary key (patient_id),
	foreign key (id) references person
		on delete cascade
	);
-- insert into patient values(1,1);
-- insert into patient values(2,2);
-- insert into patient values(2,3);
-- insert into patient values(1,4);

create table slot
	(dat date,
	start_time time,
	primary key (dat,start_time)
	);
-- insert into slot values('2020-04-21','12:00');
-- insert into slot values('2020-04-21','12:30');
-- insert into slot values('2020-04-21','13:00');
-- insert into slot values('2020-04-21','13:30');

-- insert into slot values('2020-04-22','12:00');
-- insert into slot values('2020-04-22','12:30');
-- insert into slot values('2020-04-22','13:00');
-- insert into slot values('2020-04-22','13:30');

create table room
	(room_no int,
	type text,
	primary key (room_no)
	);
-- insert into room values(1,'Examination');
-- insert into room values(2,'Examination');
-- insert into room values(3,'OT');
-- insert into room values(4,'Ward');
-- insert into room values(5,'Test');
-- insert into room values(6,'Test');

create table prescription
	(presc_id int,
	instr text,
	primary key (presc_id)
	);
-- insert into prescription values(1,'Sleep early');
-- insert into prescription values(2,'Sleep early');
-- insert into prescription values(3,'Sleep early');
-- insert into prescription values(4,'Sleep early');

create table bill
	(bill_no int,
	paid_by int,
	--paid int,
	--amt int,
	purpose text
		check (purpose in ('OPD','Pharmacy','Admission','Diagnosis')),
	discount int default 0
		check (discount <= 100),
	mode text
		check (mode in ('Cash','Card','Cheque','Online',NULL)),
	primary key (bill_no),
	foreign key (paid_by) references person
		on delete cascade
	);
-- insert into bill values(1,NULL,'OPD',20,'Cash');
-- insert into bill values(2,NULL,'OPD',20,'Cash');
-- insert into bill values(3,NULL,'OPD',20,'Cash');
-- insert into bill values(4,NULL,'Admission',20,'Online');
-- insert into bill values(5,NULL,'OPD',20,'Cash');
-- insert into bill values(6,NULL,'Diagnosis',10,'Cash');
-- insert into bill values(7,NULL,'Pharmacy',10,'Card');

create table appointment
	(app_id int,
	type text,
	bill_no int,
	presc_id int,
	primary key (app_id),
	foreign key (bill_no) references bill 
		on delete cascade,
	foreign key (presc_id) references prescription
		on delete cascade
	);
-- insert into appointment values(1,'OPD',1,1);
-- insert into appointment values(2,'OPD',2,2);
-- insert into appointment values(3,'OPD',3,3);
-- insert into appointment values(4,'OPD',5,4); 

create table symptom
	(symp_id int,
	symp_name text,
	primary key (symp_id)
	);
-- insert into symptom values(1,'Headache');
-- insert into symptom values(2,'Fatigue');
-- insert into symptom values(3,'Chest Pain');
-- insert into symptom values(4,'Breathing difficulty');

create table disease
	(disease_id int,
	disease_name text,
	info_link text,
	primary key (disease_id)
	);
-- insert into disease values(1,'Hypertension');
-- insert into disease values(2,'Migrane');
-- insert into disease values(3,'Back pain');
-- insert into disease values(4,'Anxiety');
-- insert into disease values(5,'Obesity');

create table bed
	(bed_no int,
	type text,
	charges int,
	room_no int,
	primary key (bed_no),
	foreign key (room_no) references room
		on delete cascade
	);
-- insert into bed values(1,'Normal',300,4);
-- insert into bed values(2,'Normal',300,4);
-- insert into bed values(3,'Normal',300,4);
-- insert into bed values(4,'Normal',300,4);

create table test
	(test_id int,
	name text,
	charges int,
	--eqp_id int,
	--foreign key (eqp_id) references equipment
	--	on delete cascade,
	primary key (test_id)
	);
-- insert into test values(1,'Blood test',200);
-- insert into test values(2,'MRI',6000);
-- insert into test values(3,'X-Ray',500);

create table equipment
	(eqp_id int,
	type text,
	room_no int,
	test_id int,
	primary key (eqp_id),
	foreign key (room_no) references room
		on delete cascade,
	foreign key (test_id) references test
		on delete cascade
	);
-- insert into equipment values(1,'MRI1',5,2);
-- insert into equipment values(2,'X-Ray1',6,3);

create table medicine
	(med_id int,
	name text,
	descr text,
	manufc text,
	price int,
	--expiry_dt date,
	--mfg_dt date,
	primary key (med_id)
	);
-- insert into medicine values(1,'Aspirin','dawa','Zydus',10);
-- insert into medicine values(2,'Vitamin C','dawa','Neo',50);
-- insert into medicine values(3,'Riboflavin','dawa','Nostrum',30);
-- insert into medicine values(4,'Tetracycline','dawa','Pharm',100);

create table doctor_room_slot
	(doc_id int,
	room_no int,
	--slot_id int,
	dat date,
	start_time time,
	primary key (doc_id,dat,start_time),  ----room_no confusiom
	foreign key (doc_id) references doctor
		on delete cascade,
	foreign key (room_no) references room
		on delete cascade,
	foreign key (dat,start_time) references slot
		on delete cascade
	);
-- insert into doctor_room_slot values(4,1,'2020-04-21','12:00');
-- insert into doctor_room_slot values(4,1,'2020-04-21','12:30');
-- insert into doctor_room_slot values(4,1,'2020-04-22','12:00');
-- insert into doctor_room_slot values(4,1,'2020-04-22','12:30');
-- insert into doctor_room_slot values(5,2,'2020-04-21','12:00');
-- insert into doctor_room_slot values(5,2,'2020-04-21','12:30');
-- insert into doctor_room_slot values(5,2,'2020-04-22','12:00');
-- insert into doctor_room_slot values(5,2,'2020-04-22','12:30');

create table handle
	(staff_id int,
	eqp_id int,
	primary key (staff_id, eqp_id),
	foreign key (staff_id) references support_staff
		on delete cascade,
	foreign key (eqp_id) references equipment
		on delete cascade
	);
-- insert into handle values(8,1);
-- insert into handle values(9,2);

create table meet
	(app_id int,
	patient_id int,
	doc_id int,
	--slot_id int,
	dat date,
	start_time time,
	patient_complaint text,
	primary key (doc_id, dat, start_time),
	foreign key	(app_id) references appointment
		on delete cascade,
	foreign key (patient_id) references patient
		on delete cascade,
	foreign key (doc_id,dat,start_time) references doctor_room_slot
		on delete cascade
	);
-- insert into meet values(1,1,4,'2020-04-21','12:00',NULL);
-- insert into meet values(2,2,5,'2020-04-21','12:00',NULL);
-- insert into meet values(3,3,5,'2020-04-22','12:00',NULL);
-- insert into meet values(4,4,4,'2020-04-22','12:00',NULL);

create table history
	(person_id int,
	disease_id int,
	prev_hist_link text,
	detected date,
	primary key (person_id,disease_id),
	foreign key (person_id) references person
		on delete cascade,
	foreign key (disease_id) references disease
		on delete cascade
	);
-- insert into history values(1,1,'','2020-01-01');
-- insert into history values(2,2,'','2020-04-01');

create table suffers
	(patient_id int,
	disease_id int,
	primary key (patient_id,disease_id),
	foreign key (patient_id) references patient
		on delete cascade,
	foreign key (disease_id) references disease
		on delete cascade
	);
-- insert into suffers values(1,3);
-- insert into suffers values(2,1);

create table shows
	(app_id int,
	symp_id int,
	primary key (app_id, symp_id),
	foreign key (app_id) references appointment
		on delete cascade,
	foreign key (symp_id) references symptom
		on delete cascade
	);
-- insert into shows values(1,2);
-- insert into shows values(2,3);
-- insert into shows values(3,3);

create table takes
	(patient_id int,
	test_id int,
	result_file text,
	comments text,
	dat date,
	bill_no int,
	primary key (patient_id,test_id,dat),
	foreign key (bill_no) references bill
		on delete cascade,
	foreign key (patient_id) references patient
		on delete cascade,
	foreign key (test_id) references test
		on delete cascade
	);
-- insert into takes values(1,1,'foo.com','NP','2021-04-01',6);

create table should_take
	(presc_id int,
	test_id int,
	primary key (presc_id,test_id),
	foreign key (presc_id) references prescription
		on delete cascade,
	foreign key (test_id) references test
		on delete cascade
	);
-- insert into should_take values(1,1);

create table bill_med
	(bill_no int,
	med_id int,
	qty int,
	primary key (bill_no, med_id),
	foreign key (bill_no) references bill
		on delete cascade,
	foreign key (med_id) references medicine
		on delete cascade
	);
-- insert into bill_med values(7,1,10);
-- insert into bill_med values(7,2,15);

create table occupies
	(patient_id int,
	bed_no int,
	start_dt date,
	end_dt date,
	bill_no int,
	primary key (patient_id),
	foreign key (patient_id) references patient
		on delete cascade,
	foreign key (bed_no) references bed
		on delete cascade,
	foreign key (bill_no) references bill
		on delete cascade
	);
-- insert into occupies values(3,1,'2021-04-22',NULL,NULL);

create table meds
	(med_id int,
	presc_id int,
	dosage text,
	frequency text,
	primary key (med_id,presc_id),
	foreign key (med_id) references medicine
		on delete cascade,
	foreign key (presc_id) references prescription
		on delete cascade
	);
-- insert into meds values(1,1,'','Need');
-- insert into meds values(2,1,'','W');

create table assg_to
	(staff_id int,
	room_no int,
	primary key (staff_id),
	foreign key (staff_id) references support_staff
		 on delete cascade,
	foreign key (room_no) references room
		on delete cascade
	);
-- insert into assg_to values(6,4);

create table visits
	(patient_id int,
	--bed_id int,
	doc_id int,
	visit_dat timestamp,
	visit_notes text,
	--primary key (patient_id,bed_id,doc_id,visit_dat),
	--foreign key (patient_id,bed_id) references occupies
	primary key (patient_id,doc_id,visit_dat),
	foreign key (patient_id) references occupies
		on delete cascade,
	foreign key (doc_id) references doctor
		on delete cascade
	);
-- insert into visits values(3,5,'2020-04-22',NULL);
