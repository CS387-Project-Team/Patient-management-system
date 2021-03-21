-- do this 7 times in python at the stroke of midnight on Sunday night 
-- this copies over all slots of the latest week 
-- assumption is that our data starts from a complete week (mon morn)

insert into slot
	select max(dat)+1, start_time
	from slot
	group by start_time;

with free_rooms (room_no) as ((select room_no from room) except (select room_no from doctor_room_slot where (dat, start_time) = ($1, $2))) select count(*) from free_rooms; --=> check whether there is a room available for the slot the doc wants to add. If not, say sorry to the doctor and that there is no room available.

--If rooms are available, 
with free_rooms (room_no) 
as ((select room_no from room) 
		except 
	(select room_no from doctor_room_slot where (dat, start_time) = ('2020-01-01', '10:30'))), 
chosen_room(room_no) as 
(select min(room_no) from free_rooms) 
insert into doctor_room_slot select 1, room_no, '2020-01-01', '10:30' from chosen_room;