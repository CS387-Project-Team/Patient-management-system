create table person
	(id int,
	name varchar(30),
	address text,
	pincode int,
	contact varchar(30),
	gender varchar(2),
	age int,
	username varchar(30),
	password varchar(30),
	email_id varchar(30),
	primary key(id)
	);

create table doctor
	(id int,
	speciality text
		check (speciality in {'Physician','Cardiology','Nephrology','Orthopaedic','Skin','Neurology'}),
	qualification text,
	salary int,
	permanent int,
	experience int,
	opd_charges int,
	ot_charges int
	primary key(id),
	foreign key (id) references person
		on delete set null
	);

create table support_staff
	(id int,
	type text,
	qualification text,
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
	qualification text,
	role varchar(10),
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
	(symptom_id int,
	name text,
	primary key (symptom_id)
	);

create table disease
	(disease_id int,
	name varchar(20),
	info_link text,
	primary key (disease_id)
	);

create table test
	(test_id int,
	name varchar(30),
	charges int,
	primary key (id)
	);

create table bed
	(bed_no int,
	type varchar(20),
	charges int,
	primary key (bed_no)
	);

create table equipment
	(eqp_id int,
	type text,
	primary key (id)
	);

create table medicine
	(med_id int,
	name varchar(30),
	descr text,
	manufc text,
	price int,
	expiry_dt date,
	mfg_dt date,
	primary key (id)
	);

create table event
	(event_id int,
	name varchar(30),
	start_dt timestamp,
	end_dt timestamp,
	descr text,
	link text,
	primary key (id)
		);

create table bill
	(bill_no int,
	paid int,
	purpose text,
	discount int,
	primary key (id)
	);

create table participate
	(person_id int,
	event_id int,
	primary key (person_id,event_id),
	foreign key (person_id) references person
		on delete cascade
	);

create table organised
	(person_id int,
	event_id int,
	primary key (person_id,event_id),
	foreign key (person_id) references person
		on delete cascade
	);

create table doc_in_chrg
	(id int,
		);