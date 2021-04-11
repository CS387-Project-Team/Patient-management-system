--update inventory
--1) add/ remove beds
insert into bed
values(10,'Type1',1000,20)

delete from bed
where bed_no = 10

--check if bed exists already

insert into room
	values(10,'NICU')

--2) add new equipments
insert into equipment
	values(10,'CT Scan',20,1)

--3) add new medicines
insert into medicine
	values(10,'Calpol','Paracetamol, Fever relief','Cipla',50)

--check if med exists already