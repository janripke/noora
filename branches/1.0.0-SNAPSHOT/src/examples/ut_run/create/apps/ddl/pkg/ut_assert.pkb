create or replace package body UT_ASSERT as

  function bool_to_char(a in boolean) return varchar2 is
  begin
    if a = true
    then
      return 'true';
    end if;
    if a = false
    then
      return 'false';
    end if;
  
    return chr(0);
  end;

  procedure equals(p_message in varchar2
                  ,a       in varchar2
                  ,b       in varchar2) is
  begin
  
    if nvl(a, chr(0)) <> nvl(b, chr(0))
    then
      raise_application_error(-20001, p_message || ' expected ' || nvl(a, 'null') || ' was ' || nvl(b, 'null'));
    end if;
  end;

  procedure equals(p_message in varchar2
                  ,a       in boolean
                  ,b       in boolean) is
  begin
    equals(p_message, bool_to_char(a), bool_to_char(b));
  end;

  procedure not_equals(p_message in varchar2
                      ,a       in varchar2
                      ,b       in varchar2) is
  begin
  
    if nvl(a, chr(0)) = nvl(b, chr(0))
    then
      raise_application_error(-20002, p_message || ' expected ' || nvl(a, 'null') || ' was ' || nvl(b, 'null'));
    end if;
  end;

  procedure not_equals(p_message in varchar2
                      ,a       in boolean
                      ,b       in boolean) is
  begin
    not_equals(p_message, bool_to_char(a), bool_to_char(b));
  end;

  procedure throws(p_message varchar2
                  ,a         varchar2
                  ,b         varchar2) is
    no_exception exception;
    l_sqlerrm varchar2(4000);
  begin
  
    execute immediate a;
  
    raise no_exception;
  
  exception
  
    when no_exception then
      raise_application_error(-20003, p_message || ' expected ' || 'null' || ' was ' || nvl(b, 'null'));
    
    when others then
      l_sqlerrm := sqlerrm;
      if instr(l_sqlerrm, chr(10), 1, 1) > 0
      then
        l_sqlerrm := trim(substr(l_sqlerrm, 1, instr(l_sqlerrm, chr(10), 1, 1) - 1));
      end if;
      if nvl(trim(l_sqlerrm), chr(0)) <> b
      then
      
        raise_application_error(-20003, p_message || ' expected ' || nvl(l_sqlerrm, 'null') || ' was ' || nvl(b, 'null'));
      end if;
    
  end;

end UT_ASSERT;
/
