whenever SQLERROR exit 1
whenever OSERROR exit
set serveroutput off
set termout off
spool feedback.log
declare
  cursor c_user_objects is
    select object_name, object_type
    from user_objects
    where object_name like 'UT_%'
    and object_name not in ('UT_RUN','UT_ASSERT')
    and object_type='PACKAGE BODY'
    order by object_type;

  statement varchar2(1024);
  M_QUOTE	constant varchar2(256):=chr(39);

begin

  for user_object in c_user_objects loop
    statement:='begin ut_run.run(' || M_QUOTE || user_object.object_name || M_QUOTE || '); end;';
    dbms_output.put_line(statement);
    execute immediate statement;
  end loop;

end;
/
