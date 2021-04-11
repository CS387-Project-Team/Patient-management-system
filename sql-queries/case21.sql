--Disease_Symptom
--1) Only symptom
select distinct(name)
from ((((((suffers natural join dis)
		natural join patient)
		natural join meet)
		natural join appointment)
		natural join shows)
		natural join symptom)

--2) Symptom with %
with dis(disease_id) as 
(select id 
	from disease 
	where name = 'Covid'),
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
