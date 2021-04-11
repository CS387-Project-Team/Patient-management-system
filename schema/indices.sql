-- Required when patient wants to book an appointment
-- Slots are used to find the relevant slots of the doctor.
-- Frequency of reading is much higher than frequency of updates / inserts
create index "slot.dat"
    on slot
    using btree
    (dat);

-- Used to eliminate the slots which have already been booked
-- Frequency of reading is much higher than frequency of updates / inserts
-- The reason is that at any time a patient will look at free slots of several doctors, but fix an appointment with only one doctor.
create index "meet.doc_dat"
    on meet
    using btree
    (doctor_id, dat);

-- Used when patient searched for relevant doctors while booking appointments.
-- Used by admin to find doctors of a particular speciality.
-- Frequency of reading is much higher than frequency of updates / inserts
create index "doctor.speciality"
    on doctor
    using btree
    (speciality);

-- Used by admin to find doctors by salary.
-- Frequency of reads is higher than inserts or updates, cause this will be used every month to manage accounts of the hospital.
-- However, a new doctor or a change in salary is a rare event.
create index "doctor.salary"
    on doctor
    using btree
    (salary);

-- Used by patient to book a new test.
-- Used by support staff to generate bill.
-- Frequency of reading is much higher than frequency of updates / inserts
create index "test.name"
    on test
    using btree
    (name);

-- Used by patient to view which tests have been taken by him in the past or to view his upcoming tests.
-- Frequency of reading is much higher than frequency of updates / inserts
create index "takes.test_id"
    on takes
    using btree
    (test_id);

-- Used by doctor to read about a disease when needed.
-- Used by doctor to fill prescription.
-- Used for data analytics (to find relations between diseases and other things like symptoms, pin codes (location), etc.)
-- Frequency of reading is much higher than frequency of updates / inserts
create index "disease.name"
    on disease
    using btree
    (name);

-- Used by doctor to read about a new symptom
-- Used by doctor to fill prescription.
-- Used for data analytics (to find the relations between diseases and symptoms)
-- Frequency of reading is much higher than frequency of updates / inserts
create index "symptom.name"
    on symptom
    using btree
    (name);

-- Used by admin to find support staff by salary.
-- Frequency of reads is higher than inserts or updates, cause this will be used every month to manage accounts of the hospital.
-- However, change in salary is a rare event.
create index "support_staff.salary"
    on support_staff
    using btree
    (salary);