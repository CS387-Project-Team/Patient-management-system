
-- Use case: Allot bed to patient

-- shows all room types
select distinct type from room where type is not null;

-- shows all room types
select distinct type from bed where type is not null;

-- if this returns 0, display pop-up. 
with free_beds(bed_no) as 
	((select bed_no from bed natural join room where bed.type = '1' and room.type = '2')
		except 
		(select bed_no from bed natural join room natural join occupies where bed.type = '1' and room.type = '2' and end_dt is null)) 
select count(*) from free_beds;


-- this adds an entry into the occupies table. Current date and patient id need to be passed to it. Bill id and end dt will be taken care of later.
with free_beds(bed_no) as 
	((select bed_no from bed natural join room where bed.type = '1' and room.type = '2') 
		except 
		(select bed_no from bed natural join room natural join occupies where bed.type = '1' and room.type = '2' and end_dt is null)) 
insert into occupies select 1, min(bed_no), '2020-01-01' from free_beds;
