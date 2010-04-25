create or replace package body ut_app_prop as

  procedure setup is
  begin
    null;
  end;
  
  procedure teardown is
  begin
    rollback;
  end;
  
  function ins_property
    (p_name in varchar2
    ,p_value in varchar2) return number is
    
    l_id number(12);
    
  begin
    insert into application_properties 
      (name
      ,value)
    values
      (p_name
      ,p_value) 
    returning id into l_id;
    
    return l_id;
  end;
  
  
  -- this test is successful when the insert property is retrieved.
  -- remarks: on line 45 i made an error, so this test will always fail.
  --          this is to show what happens if a unittest fails, when
  --          you use the unittest.py script, to run the unittests.
  procedure t_get_property_pass is
  
    l_id number(12);
    l_value varchar2(4000);
  
  begin
    l_id:=ins_property('test.code','test.code');
    ut_assert.not_equals('[t_get_property], invalid property id:',l_id,null);
    l_value:=app_prop.get_property('test.code');
    ut_assert.equals('[t_get_property], invalid property value:',l_value,'test1.code');
    rollback; 
  end;


end ut_app_prop;
/
