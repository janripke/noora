whenever SQLERROR exit 1
whenever OSERROR exit 2
spool feedback.log
declare
  cursor c_user_objects is
    select unique package_name
    from   all_arguments a
    where  substr(a.object_name,1,2) = 'T_';

  statement varchar2(1024);
  M_QUOTE	constant varchar2(256):=chr(39);

begin

  for user_object in c_user_objects loop
    statement:='begin ut_run.run(' || M_QUOTE || user_object.package_name || M_QUOTE || '); end;';
    dbms_output.put_line(statement);
    execute immediate statement;
  end loop;

end;
/
