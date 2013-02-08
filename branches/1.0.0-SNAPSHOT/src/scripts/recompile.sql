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

  for user_object in c_user_objects loop
    dbms_output.put_line(user_object.object_name);
    if user_object.object_type='PACKAGE' then
      statement:='alter package ' || M_DQUOTE || user_object.object_name || M_DQUOTE ||  ' compile';
      execute(statement);
    end if;
    
    if user_object.object_type='PACKAGE BODY' then
      statement:='alter package ' || M_DQUOTE || user_object.object_name || M_DQUOTE || ' compile body';
      execute(statement);
    end if;

    if user_object.object_type='TRIGGER' then
      statement:='alter trigger ' || M_DQUOTE || user_object.object_name || M_DQUOTE || ' compile';
      execute(statement);
    end if; 

    if user_object.object_type='VIEW' then
      statement:='alter view ' || M_DQUOTE || user_object.object_name || M_DQUOTE || ' compile';
      execute(statement);
    end if; 
    
  end loop;

end;
/
