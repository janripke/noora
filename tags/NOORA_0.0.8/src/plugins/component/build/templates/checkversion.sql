set serveroutput off
set termout off
set feedback off
set echo off
set showmode off
define expected_version=to_char('&2')
declare

  database_version	varchar2(256);

  function get_database_version return varchar2 is

    l_value	varchar2(256);

  begin
    execute immediate '&3' into l_value;

    return l_value;

  exception    
    when no_data_found then
      return 'Nothing';
    when others then
      return 'Nothing';

  end;

  


begin

  database_version:=get_database_version;  
  if nvl(database_version,chr(0))<>nvl(&expected_version,chr(0)) then
    raise_application_error(-20000,'incorrect component version, expected ' || &expected_version || ' was ' || database_version);   
  end if;

end;
/
