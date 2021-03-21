-- to display free rooms in the selection box.
(select room_no from room) 
except 
(select room_no from doctor_room_slot where (dat, start_time) = ($1, $2));

--to update the row in the table
update doctor_room_slot 
set room_no = $1 where (doc_id, dat, start_time) = ($2, $3, $4);
