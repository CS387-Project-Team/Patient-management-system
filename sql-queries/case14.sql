-- Use case: Fill prescription, disease, symptoms after an appointment

-- Show all appointments of this doc so that they can choose which appointment to exter info for
select * from meet where doc_id = 4;

-- Show all symptoms in the database, UI will have a multi select box 
select * from symptom;

-- Add symptoms diagnosed in an appointment
insert into shows select '$cur_app_id', sypm_id from '$symptoms_selected';  

-- Show all diseases in the database, UI will have a multi select box 
select * from disease;

-- Add diseases the patient is suffering  
insert into suffers select '$cur_patient_id', id from '$diseases_selected'; 


-- Generate prescription 
insert into prescription select max(presc_id)+1 from prescription;

-- Link this prescription with the appointment 
with cur_presc(cur_presc_id) as  
	(select max(presc_id) from prescription)
update appointment
	set presc_id = cur_presc_id from cur_presc where app_id = '$cur_app_id';

-- Show all medicines in the database, UI will have a multi select box 
select * from medicine;

-- Prescribe some medicines, iterate over seletion made
insert into meds values ('med_id', 'presc_id', $1, $2);

-- Show all tests, UI will have a multi select box
select * from test; 

-- Suggest tests
insert into should_take values ('presc_id', 'test_id');
