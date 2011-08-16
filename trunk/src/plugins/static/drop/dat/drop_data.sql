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
    
  cursor c_constraints_by_type(b_table_name varchar2, b_constraint_type varchar2) is
    select constraint_name
    from   user_constraints
    where  table_name      = b_table_name
    and    constraint_type = b_constraint_type;

  statement	      varchar2(1024);
  table_name      varchar2(256);
  constraint_name varchar2(256);
  M_DQUOTE        varchar2(1):='"';
  
begin
	dbms_output.put_line('Disabling all constraints');
	for user_object in c_user_objects loop
	  table_name:=user_object.table_name;
    for constraint in c_constraints(table_name) loop
      statement:='ALTER TABLE ' || table_name || ' disable constraint ' || M_DQUOTE || constraint.constraint_name || M_DQUOTE || ' cascade';
      --dbms_output.put_line(statement);
      execute immediate statement;
    end loop;
  end loop;
  --
  dbms_output.put_line('Removing all data');
  for user_object in c_user_objects loop
    table_name:=user_object.table_name;
    statement:='TRUNCATE TABLE ' || M_DQUOTE || user_object.table_name || M_DQUOTE; 
    --dbms_output.put_line(statement);
    execute immediate statement;    
  end loop;
  --
  dbms_output.put_line('Enabling the constraints');
  for user_object in c_user_objects loop
    table_name:=user_object.table_name;    
    dbms_output.put_line('Enabling the primary constraints');
    for constraint in c_constraints_by_type(table_name, 'P') loop
      statement:='ALTER TABLE ' || table_name || ' enable constraint ' || M_DQUOTE || constraint.constraint_name || M_DQUOTE;
      dbms_output.put_line(statement);
      execute immediate statement;
    end loop;
    
   
    
    
  end loop;
  
  
  for user_object in c_user_objects loop
    table_name:=user_object.table_name;    
    dbms_output.put_line('Enabling all the constraints');
    for constraint in c_constraints(table_name) loop
      statement:='ALTER TABLE ' || table_name || ' enable constraint ' || M_DQUOTE || constraint.constraint_name || M_DQUOTE;
      dbms_output.put_line(statement);
      execute immediate statement;
    end loop;
  end loop;  
  
end;
/
set serveroutput off
