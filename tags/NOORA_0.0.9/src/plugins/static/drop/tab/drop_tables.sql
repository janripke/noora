set serveroutput on
declare
  cursor c_user_objects is
    select table_name 
    from user_tables
    where table_name not in ('CREATE$JAVA$LOB$TABLE'); 

  cursor c_constraints(b_table_name varchar2) is
    select constraint_name 
    from user_constraints
    where table_name=b_table_name;

  statement	varchar2(1024);
  table_name    varchar2(256);
  constraint_name varchar2(256);
  M_DQUOTE      varchar2(1):='"';
  
begin
  for user_object in c_user_objects loop
    table_name:=user_object.table_name;
    --for constraint in c_constraints(table_name) loop
    --  statement:='ALTER TABLE ' || table_name || ' drop constraint ' || M_DQUOTE || constraint.constraint_name || M_DQUOTE || ' cascade';
    --  dbms_output.put_line(statement);
    --  execute immediate statement;
    -- end loop;

    statement:='DROP TABLE ' || M_DQUOTE || user_object.table_name || M_DQUOTE || ' cascade constraints purge'; 
    dbms_output.put_line(statement);
    execute immediate statement;
  end loop;
end;
/
set serveroutput off
