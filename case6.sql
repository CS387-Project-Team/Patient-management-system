-- Booking a test
insert into takes(patient_id, test_id, dat)
values ('1234', '5678', '12/03/2021');

-- Cancelling a test
delete from takes
where patient_id = '1234' and test_id = '5678';