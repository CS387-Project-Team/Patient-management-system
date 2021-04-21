--Disease_Symptom
--1) Only symptom
select distinct(symp_name)
from ((((((suffers natural join disease)
		natural join patient)
		natural join meet)
		natural join appointment)
		natural join shows)
		natural join symptom)
where dis_name = 'Back pain'

--2) Symptom with %
with dis(disease_id) as 
(select id 
	from disease 
	where dis_name = 'Back pain'),
cnt as (select sum(*) as cast(tot as real)
		from ((((((suffers natural join dis)
			natural join patient)
			natural join meet)
			natural join appointment)
			natural join shows)
			natural join symptom))
select name, count(name)/cnt
from ((((((suffers natural join dis)
		natural join patient)
		natural join meet)
		natural join appointment)
		natural join shows)
		natural join symptom)
group by name
