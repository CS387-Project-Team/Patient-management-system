--Give Admin privileges to someone
select p.name,p.id
from person as p
where p.name like '%'+'naam_nahi_hai'+'%';

--check authorization??

insert into admin
values (id,'10','Qual','admin');