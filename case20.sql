--make payment
--Med bills are paid at the time of purchase hence no unpaid med bill
with pt(patient_id) as
	(select patient_id
	from patient
	where person.id = 10) --fill correct one
(select bill_no, amt, purpose, discount
from (((meet natural join pt)
		natural join appointment)
		natural join bill_no) as foo
where person_no is null)
union
(select bill_no, amt, purpose, discount
from ((pt natural join takes)
		natural join bill)
where person_no is null)
