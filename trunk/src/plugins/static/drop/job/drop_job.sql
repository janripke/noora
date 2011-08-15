set serveroutput on
declare
  cursor c_user_objects is
    select * 
      from user_scheduler_jobs;

  statement	varchar2(1024);
  M_DQUOTE      varchar2(1):='''';
  
begin
  for user_object in c_user_objects loop
    statement:='begin dbms_scheduler.DROP_JOB(job_name =>' || M_DQUOTE || user_object.job_name || M_DQUOTE|| ',force => TRUE); end;'; 
    execute immediate statement;
  end loop;
end;
/
set serveroutput off
