set serveroutput on
declare
  cursor c_queue_tables is
     select queue_table
     from   user_queue_tables;

  statement     varchar2(1024);
  M_QUOTE       varchar2(1):=chr(39);
begin
  for user_object in c_queue_tables loop
    statement:='begin dbms_aqadm.drop_queue_table(queue_table => '|| M_QUOTE || user_object.queue_table || M_QUOTE||', force => true); end;';     
    execute immediate statement;
  end loop;
end;
/
set serveroutput off
