--Assign duties to support staff
--1)Show the current duties
select room_no
from assg_to
where staff_id = 10;

select type,eqp_id
from handle natural join equipment
where staff_id = 10;

--2) Remove from duties
delete
from assg_to
where staff_id = 10;

delete 
from handle
where staff_id = 10;

--3) Assign new duties
insert into assg_to
values (10,12)

insert into handle
values (10,4) --staff_id, eqp_id