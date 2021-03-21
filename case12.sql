-- do this 7 times in python at the stroke of midnight on Sunday night 
-- this sopies over all slots of the latest week 
-- assumption is that our data starts from a complete week (mon morn)

insert into slot
	select max(dat)+1, start_time
	from slot
	group by start_time;