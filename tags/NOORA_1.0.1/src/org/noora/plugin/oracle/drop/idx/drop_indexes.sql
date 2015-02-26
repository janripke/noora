set serveroutput on
declare
  cursor c_user_objects is
    select index_name
    from user_indexes
    where table_name not in 'CREATE$JAVA$LOB$TABLE';

  statement	varchar2(1024);
  M_DQUOTE      varchar2(1):='"';
  
begin
  for user_object in c_user_objects loop
    statement:='DROP INDEX ' || M_DQUOTE || user_object.index_name || M_DQUOTE; 
    execute immediate statement;
  end loop;
end;
/
set serveroutput off
