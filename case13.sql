--Register/remove Doctor/ support staff, modify salary, charges etc

--1) Register Doctor
insert into doctor
values (10,'Cardiology',100000,'1',10,500,5000);

--2) Remove Doctor
delete from doctor
where id = 10;

--3) Modify salary
update doctor
set salary = 150000
where id = 10;

--4) Modify charges
update doctor
set opd_charges = 550
where id = 10;

--5) Register staff
insert into support_staff
values (10,'Blood_test',2,30000,8,14,6);

--6) Remove staff
delete from support_staff
where id = 10;

--7) Modify Salary
update support_staff
set salary = 40000
where id = 10;