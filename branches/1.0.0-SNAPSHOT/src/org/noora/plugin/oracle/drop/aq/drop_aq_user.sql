set serveroutput on
declare
  cursor c_user_objects is
    select agent_name object 
    from user_aq_agent_privs;

  statement      varchar2(1024);
  M_DQUOTE      varchar2(1):='''';

begin
  for user_object in c_user_objects loop
    statement:='BEGIN DBMS_AQADM.drop_aq_agent('|| M_DQUOTE || user_object.object || M_DQUOTE||'); END;';     
    execute immediate statement;
  end loop;
end;
/
set serveroutput off