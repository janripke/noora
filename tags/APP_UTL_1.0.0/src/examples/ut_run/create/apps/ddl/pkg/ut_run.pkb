create or replace package body ut_run as

  M_OK             constant varchar2(50) := '... ok';
  M_SETUP_SUITE    constant varchar2(50) := 'setup_suite';
  M_TEARDOWN_SUITE constant varchar2(14) := 'teardown_suite';
  M_SETUP          constant varchar2(50) := 'setup';
  M_TEARDOWN       constant varchar2(50) := 'teardown';


  l_pkg_name       constant varchar2(31) default lower($$plsql_unit) || '.';
  l_obj_prefix     constant varchar2(4) default 'T|_%';
  l_escape_char    constant varchar2(1) default '|';
  
  M_LF             constant varchar2(1):=chr(10);

  function find_methods(p_package_name varchar2) return t_argument_list is
    l_object_type varchar2(30) := 'PACKAGE BODY';
  
    cursor c_all_arguments(b_package_name in varchar2) is
      select object_name
      from   all_arguments a
      where  a.package_name = upper(b_package_name)
      and substr(a.object_name,1,2) = 'T_';
  
    r_all_arguments c_all_arguments%rowtype;
    argument_list   t_argument_list;
  
  begin
  
    for r_all_arguments in c_all_arguments(p_package_name)
    loop
      argument_list(nvl(argument_list.last, 0) + 1).package_name := p_package_name;
      argument_list(argument_list.last).method_name := r_all_arguments.object_name;
    end loop;
  
    return argument_list;
  
  end;

  function method_exist
    (p_package_name varchar2
    ,p_method_name  varchar2) return boolean is
                            
   l_count  number;
   l_result boolean:=false;
   
  begin 
          
    select count(0)
    into   l_count
    from   all_arguments a
    where  a.package_name = upper(p_package_name)
    and    a.object_name  = upper(p_method_name);
             
    if l_count <> 0 then
      l_result:=true;
    end if;
    
    return l_result;
    
  end method_exist;
  
  function prepare_statement
    (p_package_name varchar2
    ,p_method_name  varchar2) return varchar2 is
        
    l_result varchar2(4000);
    
  begin
    l_result := 'BEGIN' || M_LF || p_package_name || '.' || p_method_name || ';' || M_LF || 'END;';
    return l_result;
  end;

  procedure execute_setup
    (p_package_name in varchar2) is
    
    l_statement varchar2(4000);
  
  begin
    if method_exist(p_package_name, M_SETUP) then
      l_statement := prepare_statement
        (p_package_name => p_package_name
        ,p_method_name  => M_SETUP);        
      execute immediate l_statement;
      dbms_output.put_line(lower(p_package_name) || '.' || M_SETUP || M_OK);      
    end if;  
  end execute_setup;

  procedure execute_setup_suite
    (p_package_name in varchar2) is
    
    l_statement varchar2(4000);
  
  begin
    if method_exist(p_package_name, M_SETUP_SUITE) then
      l_statement := prepare_statement
        (p_package_name => p_package_name
        ,p_method_name  => M_SETUP_SUITE);
      execute immediate l_statement;  
      dbms_output.put_line(lower(p_package_name) || '.' || M_SETUP_SUITE || M_OK);
    end if;  
  end execute_setup_suite;

  procedure execute_teardown
    (p_package_name in varchar2) is
    
    l_statement varchar2(4000);
  
  begin  
    if method_exist(p_package_name, M_TEARDOWN) then	  
      l_statement := prepare_statement
        (p_package_name => p_package_name
        ,p_method_name  => M_TEARDOWN);
      execute immediate l_statement;
      dbms_output.put_line(lower(p_package_name) || '.' || M_TEARDOWN || M_OK);      
    end if;  
  end execute_teardown;

  procedure execute_teardown_suite
    (p_package_name in varchar2) is
    
    l_statement varchar2(4000);

  begin  
    if method_exist(p_package_name, M_TEARDOWN_SUITE) then	  
      l_statement := prepare_statement
        (p_package_name => p_package_name
        ,p_method_name  => M_TEARDOWN_SUITE);
      execute immediate l_statement;
      dbms_output.put_line(lower(p_package_name) || '.' || M_TEARDOWN_SUITE || M_OK);      
    end if;
  end execute_teardown_suite;

  procedure execute_methods
    (p_package_name in varchar2) is
  
    l_statement     varchar2(4000);
    l_argument_list t_argument_list;
  
  begin
  
    l_argument_list := find_methods(p_package_name);    
  
    if l_argument_list.exists(1)
    then
      for i in l_argument_list.first .. l_argument_list.last
      loop
      
        execute_setup
          (p_package_name => p_package_name);
      
        l_statement := prepare_statement
          (p_package_name => l_argument_list(i).package_name
          ,p_method_name  => l_argument_list(i).method_name);      
        execute immediate l_statement;
      
        dbms_output.put_line(lower(p_package_name) || '.' || lower(l_argument_list(i).method_name) || M_OK);        
      
        execute_teardown(p_package_name => p_package_name);
      
      end loop;
    end if;
  
  end execute_methods;


  procedure run
    (p_package_name in varchar2) is
  
  begin
  
    execute_setup_suite
      (p_package_name => p_package_name);
  
    -- invididual setup and teardown are called inside execute_methods
    execute_methods
      (p_package_name => p_package_name);
  
    execute_teardown_suite
      (p_package_name => p_package_name);
  
    dbms_output.put_line('unittest ' || lower(p_package_name) || ' succeeded. ');
  
  exception
    when others then
      dbms_output.put_line(dbms_utility.format_error_backtrace);
      dbms_output.put_line(substr(sqlerrm, 1, 256));
    
      execute_teardown(p_package_name);
      execute_teardown_suite(p_package_name => p_package_name);
    
      raise_application_error(-20001, dbms_utility.format_error_backtrace || substr(sqlerrm, 1, 256));
      
  end run;

end ut_run;
/