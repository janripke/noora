set serveroutput on
declare
  cursor c_user_java_sources is
    select object_name
    from user_objects where object_type='JAVA SOURCE';

  cursor c_user_java_classes is
    select object_name
    from user_objects where object_type='JAVA CLASS';
    
  statement	    varchar2(1024);
  M_DQUOTE      varchar2(1):='"';

begin
  for user_java_source in c_user_java_sources loop
    statement:='DROP JAVA SOURCE ' || M_DQUOTE || user_java_source.object_name || M_DQUOTE;
    execute immediate statement;
  end loop;
  
  for user_java_class in c_user_java_classes loop
    statement:='DROP JAVA CLASS ' || M_DQUOTE || user_java_class.object_name || M_DQUOTE;
    execute immediate statement;
  end loop;
  
end;
/
set serveroutput off
