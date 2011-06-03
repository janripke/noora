set serveroutput on
declare
  cursor c_user_objects is
    select object_name 
    from user_objects
    where object_type='SEQUENCE';

  statement	varchar2(1024);
  M_DQUOTE      varchar2(1):='"';
  
begin
  for user_object in c_user_objects loop
    statement:='DROP SEQUENCE ' || M_DQUOTE || user_object.object_name || M_DQUOTE; 
    execute immediate statement;
  end loop;
end;
/
set serveroutput off
