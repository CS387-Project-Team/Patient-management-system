--View generic info about hospital

--1) View doctors
select name, speciality, experience, opd_charges, ot_charges
from doctor,person 
where doc_id = id
order by speciality asc, name asc

--2) View staff
select role, count(staff_id)
from support_staff
group by role

--3) Departments
select speciality, count(doc_id)
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
select type, count(bed_no)
from bed
group by type