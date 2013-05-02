declare
  type reftype is ref cursor;
  c_ref   reftype;
  l_table varchar2(30);
begin
  open c_ref for 'select change_table_name from change_tables';
  loop
    fetch c_ref
      into l_table;
    exit when c_ref%notfound;
    execute immediate 'begin dbms_cdc_publish.drop_change_table(owner => user, change_table_name => :1, force_flag => :2); end;'
      using l_table, 'Y';
  end loop;
  close c_ref;
exception
  when others then
    null;
end;
/
