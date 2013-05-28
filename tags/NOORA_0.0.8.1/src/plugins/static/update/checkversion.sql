define expected_version=to_char('&2')
define version_statement=&3
declare

  database_version	varchar2(256);

  function get_database_version return varchar2 is

    l_value	varchar2(256);

  begin
    
    &3
 
    return l_value;

  end;

  


begin

  database_version:=get_database_version;  
  if nvl(database_version,100)<>&expected_version then
    raise_application_error(-20000,'incorrect database version');   
  end if;

end;
/
