set serveroutput on
declare
  cursor c_user_objects is
    select object_name 
    from user_objects
    where object_type='DATABASE LINK';

  statement	    varchar2(1024);
  M_QUOTE      varchar2(1):='"';
  
begin
  for user_object in c_user_objects loop
    statement:='DROP DATABASE LINK ' || M_QUOTE || user_object.object_name || M_QUOTE;     
    execute immediate statement;
  end loop;
end;
/
set serveroutput off
