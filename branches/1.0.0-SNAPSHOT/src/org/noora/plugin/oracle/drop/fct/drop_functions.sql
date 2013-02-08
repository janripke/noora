set serveroutput on
declare
  cursor c_user_objects is
    select object_name 
    from user_objects
    where object_type='FUNCTION';

  statement	varchar2(1024);
  M_DQUOTE      varchar2(1):='"';
  
begin
  for user_object in c_user_objects loop
    statement:='DROP FUNCTION ' || M_DQUOTE || user_object.object_name || M_DQUOTE; 
    dbms_output.put_line(statement);
    execute immediate statement;
  end loop;
end;
/
set serveroutput off
