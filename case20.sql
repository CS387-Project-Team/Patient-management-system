--make payment
--Med bills are paid at the time of purchase hence no unpaid med bill
with pt(patient_id) as
	(select patient_id
	from patient
	where person.id = 10) --fill correct one
((select bill_no, opd_charges, purpose, discount
from ((((meet natural join pt)
		natural join appointment)
		natural join doctor)
		natural join bill_no) as foo
where person_id is null)
union
(select bill_no, charges, purpose, discount
from (((pt natural join takes)
		natural join bill)
		natural join test)
where person_id is null))
union
(select charges*(end_dt-start_dt), purpose, discount
from (((pt natural join occupies)
		natural join bill)
		natural join bed)
where person_id is null)

--when paid
update bill
set person_id = 10
where bill_no = 1
