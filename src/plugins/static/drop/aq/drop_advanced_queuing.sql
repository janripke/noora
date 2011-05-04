set serveroutput on
declare
  cursor c_user_objects is
     select queue_table
     from   user_queue_tables;
  statement	    varchar2(1024);
  M_DQUOTE      varchar2(1):='''';
begin
  for user_object in c_user_objects loop
    statement:='BEGIN DBMS_AQADM.DROP_QUEUE_TABLE(queue_table => '|| M_DQUOTE || user_object.queue_table || M_DQUOTE||', force => true); END;';     
    execute immediate statement;
  end loop;
end;
/
set serveroutput off