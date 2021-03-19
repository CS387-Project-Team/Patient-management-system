--View generic info about hospital

--1) View doctors
select name, speciality, experience, opd_charges, ot_charges
from (doctor natural join person) as foo
order by speciality asc, name asc

--2) View staff
select role, count(id)
from support_staff
group by role

--3) Departments
select speciality, count(id)
from doctor
group by speciality

--4) Facilities

--Equipments
select distinct(type)
from equipment 

--Rooms/ Ward
select distinct(type)
from room

--Number_of_beds
select type, count(id)
from beds 
group by type