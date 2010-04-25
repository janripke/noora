create or replace package body ut_run as

  function find_methods(package_name in varchar2) return t_argument_list is
  
    cursor c_all_arguments(b_package_name in varchar2) is
      select object_name
      from   all_arguments a
      where  a.package_name = upper(b_package_name)
      and substr(a.object_name,1,2) = 'T_';
      
      
  
    r_all_arguments c_all_arguments % rowtype;
    argument_list   t_argument_list;
  
  begin
    for r_all_arguments in c_all_arguments(package_name)
    loop
    
      if lower(r_all_arguments.object_name) not in ('setup', 'teardown')
      then
        argument_list(nvl(argument_list.last, 0) + 1).package_name := package_name;
        argument_list(argument_list.last).method_name := r_all_arguments.object_name;
      end if;
    
    end loop;
  
    return argument_list;
  
  end;

  function prepare_statement(package_name in varchar2
                            ,method_name  in varchar2) return varchar2 is
  
    l_result varchar2(256);
  begin
    l_result := 'BEGIN ' || package_name || '.' || method_name || ';  END;';
    return l_result;
  end;

  procedure execute_setup(package_name in varchar2) is
  
    l_statement varchar2(256);
  begin
    l_statement := prepare_statement(package_name, 'setup');
    execute immediate l_statement;
  
    dbms_output.put_line(package_name || '.' || 'setup' || ' ... ok ');
  end;

  procedure execute_teardown(package_name in varchar2) is
  
    l_statement varchar2(256);
  begin
    l_statement := prepare_statement(package_name, 'teardown');
    execute immediate l_statement;
  
    dbms_output.put_line(package_name || '.' || 'teardown' || ' ... ok ');
  end;

  procedure execute_methods(package_name in varchar2) is
  
    l_statement     varchar2(256);
    l_argument_list t_argument_list;
  begin
    l_argument_list := find_methods(package_name);
  
    if l_argument_list.exists(1)
    then
      for i in l_argument_list.first .. l_argument_list.last
      loop
        l_statement := prepare_statement(l_argument_list(i).package_name, l_argument_list(i).method_name);
        execute immediate l_statement;
      
        dbms_output.put_line(package_name || '.' || l_argument_list(i).method_name || ' ... ok ');
      end loop;
    end if;
  
  end;

  procedure run(package_name in varchar2) is
  begin
    execute_setup(package_name);
    execute_methods(package_name);
    execute_teardown(package_name);
  
    dbms_output.put_line('unittest ' || package_name || ' succeeded. ');
  
  exception
    when others then
      dbms_output.put_line(dbms_utility.format_error_backtrace);
      dbms_output.put_line(substr(sqlerrm, 1, 256));
    
      execute_teardown(package_name);
    
      raise_application_error(-20002, dbms_utility.format_error_backtrace || substr(sqlerrm, 1, 256));
    
  end run;

end ut_run;
/
