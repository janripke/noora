declare
  cursor c_cdc_object is
    select USER user_name
         , table_name  table_name
         , 'N' force_flag
    from user_tables y
    where table_name like '%CDC%';

  statement     varchar2(1024);
  M_QUOTE       varchar2(1):=chr(39);

begin
  for cdc_object in c_cdc_object loop
    statement:='begin dbms_logmnr_cdc_publish.drop_change_table(owner => '|| M_QUOTE || cdc_object.user_name || M_QUOTE||',change_table_name => '|| M_QUOTE || cdc_object.table_name || M_QUOTE||', force_flag => '|| M_QUOTE || cdc_object.force_flag || M_QUOTE||'); end;';     
    execute immediate statement;
    dbms_output.put_line(statement);
  end loop;
end;
/
set serveroutput off