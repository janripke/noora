set serveroutput on
declare
  cursor c_queues is
     select name, queue_table
     from   user_queues;

  statement     varchar2(1024);
  M_QUOTE       varchar2(1):=chr(39);
begin
  for user_object in c_queues loop
    statement:='begin dbms_aqadm.stop_queue(queue_name => '|| M_QUOTE || user_object.name || M_QUOTE || '); end;';
    execute immediate statement;
  
    statement:='begin dbms_aqadm.drop_queue(queue_name => '|| M_QUOTE || user_object.name || M_QUOTE || '); end;';     
    execute immediate statement;

--    statement:='begin dbms_aqadm.drop_queue_table(queue_table => '|| M_QUOTE || user_object.queue_table || M_QUOTE||', force => true); end;';     
--    execute immediate statement;
    
  end loop;
end;
/
set serveroutput off
