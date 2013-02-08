define expected_environment=&2
define environment_statement=&3
declare

  database_environment	varchar2(256);

  function get_database_environment return varchar2 is

    l_value	varchar2(256);

  begin
    
    &3
 
    return l_value;

  end;

  


begin

  database_environment:=get_database_environment;  
  if nvl(database_environment,'dev')<>'&expected_environment' then
    raise_application_error(-20000,'incorrect database environment');   
  end if;

end;
/
