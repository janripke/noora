create or replace package body app_prop as

  function get_property(p_name in varchar2) return varchar2 is
    l_result varchar2(4000);
  begin
    select value
    into   l_result
    from   application_properties
    where  name = p_name;
  
    return l_result;
  exception
    when no_data_found then
      raise_application_error(-20200,'property ' || p_name || ' has no value');
  end;

end app_prop;
/
