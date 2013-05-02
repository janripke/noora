set serveroutput on
declare


  cursor c_user_objects is
    select object_name, object_type
    from user_objects
    where status<>'VALID'
    and object_name not like 'BIN%'
    order by object_type;

  statement varchar2(1024);
  M_DQUOTE      varchar2(1):=chr(34);

  procedure execute(p_statement in varchar2) is
  begin
    execute immediate p_statement;
  exception
    when others then
      null;
  end;

begin

  for user_object in c_user_objects
  loop
    if user_object.object_type in ('PACKAGE', 'PROCEDURE', 'FUNCTION', 'TRIGGER', 'VIEW')
    then
      statement := 'alter ' || user_object.object_type || ' ' || M_DQUOTE || user_object.object_name || M_DQUOTE || ' compile';
      execute(statement);
    end if;
  
    if user_object.object_type = 'PACKAGE BODY'
    then
      statement := 'alter package ' || M_DQUOTE || user_object.object_name || M_DQUOTE || ' compile body';
      execute(statement);
    end if;

    if user_object.object_type = 'JAVA SOURCE'
    then
      statement := 'alter java source ' || M_DQUOTE || user_object.object_name || M_DQUOTE || ' compile';
      execute(statement);
    end if;
    
  end loop;

end;
/
