insert into person values(0,'Admin','IITB',123456,1234567890,'M','Ramu0',crypt('Ramu0',gen_salt('bf')),'foo@gmail.com','2000-01-01','Btech');
insert into person values(1,'P0','IITB',123456,1234567890,'M','Ramu1',crypt('Ramu1',gen_salt('bf')),'foo@gmail.com','2000-01-01','Btech');
insert into person values(2,'P1','IITB',123456,1234567890,'M','Ramu2',crypt('Ramu2',gen_salt('bf')),'foo@gmail.com','2000-01-01','Btech');
insert into person values(3,'P2','IITB',123456,1234567890,'M','Ramu3',crypt('Ramu3',gen_salt('bf')),'foo@gmail.com','2000-01-01','Btech');
insert into person values(4,'D1','IITB',123456,1234567890,'M','Ramu4',crypt('Ramu4',gen_salt('bf')),'foo@gmail.com','2000-01-01','Btech');
insert into person values(5,'D2','IITB',123456,1234567890,'M','Ramu5',crypt('Ramu5',gen_salt('bf')),'foo@gmail.com','2000-01-01','Btech');
insert into person values(6,'S1','IITB',123456,1234567890,'M','Ramu6',crypt('Ramu6',gen_salt('bf')),'foo@gmail.com','2000-01-01','Btech');
insert into person values(7,'S2','IITB',123456,1234567890,'M','Ramu7',crypt('Ramu7',gen_salt('bf')),'foo@gmail.com','2000-01-01','Btech');
insert into person values(8,'S3','IITB',123456,1234567890,'M','Ramu8',crypt('Ramu8',gen_salt('bf')),'foo@gmail.com','2000-01-01','Btech');
insert into person values(9,'S4','IITB',123456,1234567890,'M','Ramu9',crypt('Ramu9',gen_salt('bf')),'foo@gmail.com','2000-01-01','Btech');

insert into doctor values(4,'Phys',22222,NULL,10,200,2000);
insert into doctor values(5,'Card',22222,NULL,10,200,2000);

insert into support_staff values(6,'Nursing',10,10000,8,14,'Mon-Fri');
insert into support_staff values(7,'Nursing',10,10000,8,14,'Mon-Fri');
insert into support_staff values(8,'Equipment',10,10000,8,14,'Mon-Fri');
insert into support_staff values(9,'Equipment',10,10000,8,14,'Mon-Fri');

insert into admin values(0,1000000);

insert into patient values(1,1);
insert into patient values(2,2);
insert into patient values(2,3);
insert into patient values(1,4);

insert into slot values('2021-04-21','12:00');
insert into slot values('2021-04-21','12:30');
insert into slot values('2021-04-21','13:00');
insert into slot values('2021-04-21','13:30');
insert into slot values('2021-04-22','12:00');
insert into slot values('2021-04-22','12:30');
insert into slot values('2021-04-22','13:00');
insert into slot values('2021-04-22','13:30');

insert into room values(1,'Examination');
insert into room values(2,'Examination');
insert into room values(3,'OT');
insert into room values(4,'Ward');
insert into room values(5,'Test');
insert into room values(6,'Test');

insert into prescription values(1,'Sleep early');
insert into prescription values(2,'Sleep early');
insert into prescription values(3,'Sleep early');
insert into prescription values(4,'Sleep early');

insert into bill values(1,NULL,'OPD',20,'Cash');
insert into bill values(2,NULL,'OPD',20,'Cash');
insert into bill values(3,NULL,'OPD',20,'Cash');
insert into bill values(4,NULL,'Admission',20,'Online');
insert into bill values(5,NULL,'OPD',20,'Cash');
insert into bill values(6,NULL,'Diagnosis',10,'Cash');
insert into bill values(7,NULL,'Pharmacy',10,'Card');

insert into appointment values(1,'OPD',1,1);
insert into appointment values(2,'OPD',2,2);
insert into appointment values(3,'OPD',3,3);
insert into appointment values(4,'OPD',5,4); 

insert into symptom values(1,'Headache');
insert into symptom values(2,'Fatigue');
insert into symptom values(3,'Chest Pain');
insert into symptom values(4,'Breathing difficulty');

insert into disease values(1,'Hypertension');
insert into disease values(2,'Migrane');
insert into disease values(3,'Back pain');
insert into disease values(4,'Anxiety');
insert into disease values(5,'Obesity');

insert into bed values(1,'Normal',300,4);
insert into bed values(2,'Normal',300,4);
insert into bed values(3,'Normal',300,4);
insert into bed values(4,'Normal',300,4);

insert into test values(1,'Blood test',200);
insert into test values(2,'MRI',6000);
insert into test values(3,'X-Ray',500);

insert into equipment values(1,'MRI1',5,2);
insert into equipment values(2,'X-Ray1',6,3);

insert into medicine values(1,'Aspirin','dawa','Zydus',10);
insert into medicine values(2,'Vitamin C','dawa','Neo',50);
insert into medicine values(3,'Riboflavin','dawa','Nostrum',30);
insert into medicine values(4,'Tetracycline','dawa','Pharm',100);

insert into doctor_room_slot values(4,1,'2021-04-21','12:00');
insert into doctor_room_slot values(4,1,'2021-04-21','12:30');
insert into doctor_room_slot values(4,1,'2021-04-22','12:00');
insert into doctor_room_slot values(4,1,'2021-04-22','12:30');
insert into doctor_room_slot values(5,2,'2021-04-21','12:00');
insert into doctor_room_slot values(5,2,'2021-04-21','12:30');
insert into doctor_room_slot values(5,2,'2021-04-22','12:00');
insert into doctor_room_slot values(5,2,'2021-04-22','12:30');

insert into handle values(8,1);
insert into handle values(9,2);

insert into meet values(1,1,4,'2021-04-21','12:00',NULL);
insert into meet values(2,2,5,'2021-04-21','12:00',NULL);
insert into meet values(3,3,5,'2021-04-22','12:00',NULL);
insert into meet values(4,4,4,'2021-04-22','12:00',NULL);

insert into history values(1,1,'','2021-01-01');
insert into history values(2,2,'','2021-04-01');

insert into suffers values(1,3);
insert into suffers values(2,1);
insert into suffers values(3,1);

insert into shows values(1,2);
insert into shows values(2,3);
insert into shows values(3,3);

insert into takes values(1,1,'foo.com','NP','2021-04-01',6);

insert into should_take values(1,1);

insert into bill_med values(7,1,10);
insert into bill_med values(7,2,15);

insert into occupies values(3,1,'2021-04-22',NULL,4);

insert into meds values(1,1,'','Need');
insert into meds values(2,1,'','W');

insert into assg_to values(6,4);

insert into visits values(3,5,'2021-04-22',NULL);