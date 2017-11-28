declare
  cursor c_cdc_object is
    select *
    from all_change_sets
    where 1=1
      and set_name <> 'SYNC_SET'
      and publisher = user 
    ;

  statement     varchar2(1024);
  M_QUOTE       varchar2(1):=chr(39);

begin
  for cdc_object in c_cdc_object loop
    statement:='begin dbms_cdc_publish.drop_change_set(change_set_name => '|| M_QUOTE || cdc_object.set_name || M_QUOTE||'); end;';     
    execute immediate statement;
  end loop;
end;
/