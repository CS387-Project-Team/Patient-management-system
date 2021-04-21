--make payment
--Med bills are paid at the time of purchase hence no unpaid med bill
with pt(patient_id) as
	(select patient_id
	from patient
	where id = 2) --fill correct one
((select bill_no, opd_charges as chg, purpose, discount
from ((((meet natural join pt)
		natural join appointment)
		natural join doctor)
		natural join bill) as foo
where paid_by is null)
union
(select bill_no, charges as chg, purpose, discount
from (((pt natural join takes)
		natural join bill)
		natural join test)
where paid_by is null))
union
(select bill_no, charges*(end_dt-start_dt) as chg, purpose, discount
from (((pt natural join occupies)
		natural join bill)
		natural join bed)
where paid_by is null and end_dt is not null)

--when paid
update bill
set person_id = 10
where bill_no = 1
