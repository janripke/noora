set serveroutput on
declare
  cursor c_user_objects is
    select object_name, object_type 
    from user_objects
    where object_type in ('PACKAGE','PACKAGE BODY')
    and object_name not like 'BIN%'
    order by object_type desc;

  statement	varchar2(1024);
  M_DQUOTE      varchar2(1):='"';
  
begin
  for user_object in c_user_objects loop
    if user_object.object_type='PACKAGE' then
      statement:='DROP PACKAGE ' || M_DQUOTE || user_object.object_name || M_DQUOTE; 
      execute immediate statement;
    elsif user_object.object_type='PACKAGE BODY' then
      statement:='DROP PACKAGE BODY ' || M_DQUOTE || user_object.object_name || M_DQUOTE; 
      execute immediate statement; 
    end if;
  end loop;
end;
/
set serveroutput off
