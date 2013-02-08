set serveroutput on
declare
  cursor c_change_tables is
    select change_table_name 
    from all_change_tables
    where change_table_schema = user()
    ; 

  statement	varchar2(1024);
  table_name    varchar2(256);
  constraint_name varchar2(256);
  M_DQUOTE      varchar2(1):='''';
  
begin
  for change_table in c_change_tables loop
    table_name:=change_table.change_table_name;
    statement:='BEGIN DBMS_CDC_PUBLISH.DROP_CHANGE_TABLE(' || M_DQUOTE || user() || M_DQUOTE ||  ',' || M_DQUOTE || table_name || M_DQUOTE || ',' || M_DQUOTE || 'Y' || M_DQUOTE || '); END;';  
    dbms_output.put_line(statement);
    execute immediate statement;
  end loop;
end;
/
set serveroutput off
