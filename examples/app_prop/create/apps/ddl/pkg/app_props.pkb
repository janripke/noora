create or replace package body app_props is

  c_pkg_name            constant varchar2(31)   := lower($$plsql_unit)||'.';

  C_FALSE constant varchar2(10) := 'false';
  C_TRUE constant varchar2(10) := 'true';
  C_NO constant varchar2(10) := 'no';
  C_YES constant varchar2(10) := 'yes';


  function get_property(p_name varchar2,
                        p_default varchar2 default null)
                        return varchar2 as
    
    r_value varchar2(4000);
  
    begin
      select value
      into   r_value
      from   application_properties
      where  name = p_name;

      return r_value;

    exception
      when no_data_found then
        if p_default is not null then
          r_value := p_default;
          return r_value;
        else 
          raise_application_error
          (-20000,'Error. Can''t find property with name: '||p_name||'...');
        end if;
    
    end;

  procedure set_property(p_name in varchar2,
                        p_value in varchar2) is
                        
    pragma autonomous_transaction;                    
   
    l_value varchar2(4000);
    begin
      l_value := get_property(p_name);
      
      if l_value <> p_value then
        update application_properties set value = p_value
        where name = p_name;
      end if;  
      
      commit;
  
  end; 

  procedure toggleValue(p_name in varchar2,
                        p_value out boolean) is
    
    pragma autonomous_transaction;
    l_value   VARCHAR2(4000);
    l_new_value varchar2(4000);

  BEGIN

     l_value := lower(app_props.get_property(p_name));
     
     case l_value
          when C_TRUE  then l_new_value := C_FALSE;
          when C_FALSE then l_new_value := C_TRUE;
          when C_YES   then l_new_value := C_NO;
          when C_NO    then l_new_value := C_YES;
          else        l_new_value := l_value; --can't toggle
        end case;

     UPDATE application_properties
     SET    value = l_new_value
     WHERE  name = p_name;
 
    COMMIT;
     
     if l_new_value = C_TRUE or l_new_value = C_YES then 
       p_value := true;
     else
       p_value := false;
     end if;   
 
  END toggleValue;

end;
/

