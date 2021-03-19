-- drop table person;
-- drop table doctor;
-- drop table support_staff;
-- drop table admin;
-- drop table patient;
-- drop table slot;
-- drop table room;
-- drop table prescription;
-- drop table appointment;
-- drop table symptom;
-- drop table disease;
-- drop table test;
-- drop table bed;
-- drop table equipment;
-- drop table medicine;
-- drop table event;
-- drop table bill;
-- drop table participate;
-- drop table organised;
-- drop table doc_in_chrg;
-- drop table doctor_room_slot;
-- drop table handle;
-- drop table meet;
-- drop table history;
-- drop table suffers;
-- drop table prescribes;
-- drop table shows;
-- drop table takes;
-- drop table should_take;
-- drop table bill_med;
-- drop table pays;
-- drop table bed_room; 
-- drop table facility;
-- drop table occupies;
-- drop table meds;
-- drop table needs;
-- drop table assg_to;
-- drop table test_bill;
-- drop table visits;

create table person
	(id int,
	name varchar(30) not NULL,
	address text,
	pincode int,
	contact varchar(10),
	gender varchar(2)
		check (gender in ('M','F',NULL)),

	username varchar(30),
	password varchar(30),
	email_id varchar(30),
	dob date,
	qualification text,
	primary key(id)
	);

create table doctor
	(id int,
	speciality text,
		--check (speciality in ("Physician","Cardiology","Nephrology","Orthopaedic","Skin","Neurology")),
	-- qualification text,
	salary int,
	permanent boolean,
	experience int,
	opd_charges int,
	ot_charges int,
	primary key (id),
	foreign key (id) references person
		on delete set null
	);

create table support_staff
	(id int,
	role text,
	-- qualification text,
	experience int,
	salary int,
	start_hr time,
	end_hr time,
	days_of_week text,
	primary key (id),
	foreign key (id) references person
		on delete set null
	);

create table admin
	(id int,
	salary int,
	-- qualification text,
	primary key (id),
	foreign key (id) references person
		on delete set null
	);

create table patient
	(id int,
	patient_id int,
	primary key (patient_id),
	foreign key (id) references person
		on delete set null
	);

create table slot
	(dat date,
	start_time time,
	primary key (dat,start_time)
	);

create table room
	(room_no int,
	type text,
	primary key (room_no)
	);

create table prescription
	(presc_id int,
	instr text,
	primary key (presc_id)
	);

create table appointment
	(app_id int,
	type text,
	primary key (app_id)
	);

create table symptom
	(id int,
	name text,
	primary key (id)
	);

create table disease
	(id int,
	name varchar(20),
	info_link text,
	primary key (id)
	);

create table test
	(test_id int,
	name varchar(30),
	charges int,
	primary key (test_id)
	);

create table bed
	(bed_no int,
	type varchar(20),
	charges int,
	primary key (bed_no)
	);

create table equipment
	(id int,
	type text,
	primary key (id)
	);

create table medicine
	(id int,
	name varchar(30),
	descr text,
	manufc text,
	price int,
	expiry_dt date,
	mfg_dt date,
	primary key (id)
	);

create table event
	(id int,
	name varchar(30),
	start_dt timestamp,
	end_dt timestamp,
	descr text,
	link text,
	primary key (id)
		);

create table bill
	(bill_no int,
	person_id int,
	paid int,
	purpose text,
	discount int,
	primary key (bill_no),
	foreign key (person_id) references person_id
		on delete cascade
	);

create table participate
	(person_id int,
	event_id int,
	primary key (person_id,event_id),
	foreign key (person_id) references person
		on delete cascade,
	foreign key (event_id) references event
		on delete cascade
	);

create table organised
	(person_id int,
	event_id int,
	primary key (person_id,event_id),
	foreign key (person_id) references person
		on delete cascade,
	foreign key (event_id) references event
		on delete cascade
	);

create table doc_in_chrg
	(doc_id int,
	event_id int,
	primary key (doc_id, event_id),
	foreign key (doc_id) references doctor
		on delete cascade,
	foreign key (event_id) references event
		on delete cascade
	);

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

create table handle
	(staff_id int,
	eqp_id int,
	primary key (staff_id, eqp_id),
	foreign key (staff_id) references support_staff
		on delete cascade,
	foreign key (eqp_id) references equipment
		on delete cascade
	);

create table meet
	(app_id int,
	patient_id int,
	doc_id int,
	--room_no int,
	--slot_id int,
	dat date,
	start_time time,
	patient_complaint text,
	primary key (app_id, patient_id, doc_id,dat,start_time),
	foreign key	(app_id) references appointment
		on delete cascade,
	foreign key (patient_id) references patient
		on delete cascade,
	foreign key (doc_id,dat,start_time) references doctor_room_slot
		on delete cascade
	);

create table history
	(person_id int,
	disease_id int,
	prev_hist_link text,
	duration text,
	primary key (person_id,disease_id),
	foreign key (person_id) references person
		on delete cascade,
	foreign key (disease_id) references disease
		on delete cascade
	);

create table suffers
	(patient_id int,
	disease_id int,
	primary key (patient_id,disease_id),
	foreign key (patient_id) references patient
		on delete cascade,
	foreign key (disease_id) references disease
		on delete cascade
	);

create table prescribes
	(app_id int,
	presc_id int,
	primary key (app_id),
	foreign key (app_id) references appointment
		on delete cascade,
	foreign key (presc_id) references prescription
		on delete cascade
	);

create table shows
	(app_id int,
	symp_id int,
	primary key (app_id, symp_id),
	foreign key (app_id) references appointment
		on delete cascade,
	foreign key (symp_id) references symptom
		on delete cascade
	);

create table takes
	(patient_id int,
	test_id int,
	result_file text,
	comments text,
	dat date,
	primary key (patient_id,test_id),
	foreign key (patient_id) references patient
		on delete cascade,
	foreign key (test_id) references test
		on delete cascade
	);

create table should_take
	(presc_id int,
	test_id int,
	primary key (presc_id,test_id),
	foreign key (presc_id) references prescription
		on delete cascade,
	foreign key (test_id) references test
		on delete cascade
	);

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

create table pays
	(person_id int,
	bill_no int,
	mode text,
	primary key (person_id, bill_no),
	foreign key (person_id) references person
		on delete cascade,
	foreign key (bill_no) references bill
		 on delete cascade
	);

create table bed_room 
	(bed_no int,
	room_no int,
	primary key (bed_no),
	foreign key (bed_no) references bed
		on delete cascade,
	foreign key (room_no) references room
		on delete cascade
	);

create table facility
	(room_no int,
	eqp_id int,
	primary key (room_no,eqp_id),
	foreign key (room_no) references room
		on delete cascade,
	foreign key (eqp_id) references equipment
		on delete cascade
	);

create table occupies
	(patient_id int,
	bed_id int,
	start_dt date,
	end_dt date,
	primary key (patient_id),
	foreign key (patient_id) references patient
		on delete cascade,
	foreign key (bed_id) references bed
		on delete cascade
	);

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

create table needs
	(test_id int,
	eqp_id int,
	primary key (test_id, eqp_id),
	foreign key (test_id) references test
		on delete cascade,
	foreign key (eqp_id) references equipment
		on delete cascade
	);

create table assg_to
	(supp_id int,
	room_no int,
	primary key (supp_id),
	foreign key (supp_id) references support_staff
		 on delete cascade,
	foreign key (room_no) references room
		on delete cascade
	);

create table test_bill
	(bill_no int,
	patient_id int,
	test_id int,
	primary key (bill_no,patient_id,test_id),
	foreign key (bill_no) references bill
		on delete cascade,
	foreign key (patient_id, test_id) references takes
		on delete cascade
	);

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