create or replace package body ut_validator as  

  M_PACKAGE_NAME           constant varchar2(50) :=lower($$plsql_unit);
  M_JOB_PREFIX             constant varchar2(255):='UT_VALIDATOR';  
  

  procedure teardown is
  begin
    rollback;
  end;
  
  function insert_mapping
    (p_mapping     in sr_mapping%rowtype) 
    return sr_mapping%rowtype is

    l_prc_name            varchar2(255)    := 'insert_mapping';
    l_mapping             sr_mapping%rowtype := p_mapping;
    l_id                  number(12);

  begin

    insert into sr_mapping
      (name
      ,value)
    values
      (p_mapping.name
      ,p_mapping.value)
    returning id into l_mapping.id;

    return l_mapping;

  end;
  
  procedure t_to_mappings_pass is
    l_prc_name          varchar2(256):='[t_to_mappings_pass]';
    l_mappings          validator.t_mappings;
    l_mapping           sr_mapping%rowtype;
    l_job_name          varchar2(256);
  begin
  
    l_job_name:= app_utl.get_job_name(p_prefix => M_JOB_PREFIX);
    logger.info(l_job_name, M_PACKAGE_NAME, l_prc_name, 'started');    
  
  
    l_mapping.name:='mapping.test';
    l_mapping.value:='vr_selection_stage.account_number = vr_selection.account_number';
    l_mapping:=insert_mapping
      (p_mapping => l_mapping);

    l_mapping.name:='mapping.test';
    l_mapping.value:='vr_selection_stage.active = vr_selection.active';
    l_mapping:=insert_mapping
      (p_mapping => l_mapping);

    l_mappings:=validator.to_mappings
      (p_job_name => l_job_name
      ,p_mapping  => 'mapping.test');
      
    ut_assert.equals(l_prc_name||', to_mappings failed :',2, l_mappings.count);
    ut_assert.equals(l_prc_name||', to_mappings failed, invalid source :','vr_selection_stage.account_number', l_mappings(1).source);
    
    rollback;
  end;    
  
  procedure t_validate_fail is
    l_prc_name          varchar2(255):='[t_validate_fail]';
  begin
    rollback;
  end;
  
  procedure t_validate_pass is                            
    l_prc_name          varchar2(255):='[t_validate_pass]';   
       
  begin
 
    rollback;
  
  end;
  
  

  
end ut_validator;
/
