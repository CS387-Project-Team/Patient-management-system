--Disease vs Area
--1) All pincodes
with pt as 
	(select patient_id, pincode
	from patient natural join person)
select pincode, name, count(*) as cnt
from ((suffers natural join pt)
		natural join disease)
group by pincode, name
order by pincode asc, cnt desc

--2) specified pincode
with pt as 
	(select patient_id
	from patient natural join person
	where pincode = 400096)
select name, count(*) as cnt
from ((suffers natural join pt)
		natural join disease)
group by name
order by cnt desc