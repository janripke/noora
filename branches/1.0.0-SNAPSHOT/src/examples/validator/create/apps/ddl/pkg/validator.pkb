create or replace package body validator as

  M_PACKAGE_NAME     constant varchar2(256):=lower($$plsql_unit);
  M_JOB_PREFIX             constant varchar2(255):='VALIDATOR';

 

  -- stage.account_number = target.account_number
  -- stage.proposition    = target.proposition
  
  
  function to_mappings
    (p_job_name   in varchar2
    ,p_mapping    in varchar2) return t_mappings is

    cursor c_mappings(b_mapping varchar2) is
      select value 
      from   sr_mapping
      where  name = b_mapping;
      
    l_mapping  t_mapping;
    l_mappings t_mappings;
    l_source   varchar2(256);
    l_target   varchar2(256);

  begin
    for r_mapping in c_mappings(p_mapping) loop
      l_source:=app_utl.get_column(r_mapping.value,'=',1);
      l_mapping.source_table_name:=app_utl.get_column(l_source,'.',1);
      l_mapping.source_column_name:=app_utl.get_column(l_source,'.',2);
      
      l_target:=app_utl.get_column(r_mapping.value,'=',2);
      l_mapping.target_table_name:=app_utl.get_column(l_target,'.',1);
      l_mapping.target_column_name:=app_utl.get_column(l_target,'.',2);
      
      l_mappings(l_mappings.count + 1):=l_mapping;
    end loop;   
    return l_mappings;   
    
  end;
  
  
  function assemble_statement
    (p_job_name           in varchar2
    ,p_table_name         in varchar2
    ,p_validate_table_name in varchar2) return varchar2 is
    
    l_statement         varchar2(4000);
    l_prc_name          varchar2(50):='assemble_statement';
    l_job_name          varchar2(256);
  begin
    if p_job_name is null then
      l_job_name:=app_utl.get_job_name(p_prefix => M_JOB_PREFIX);   
    end if;         
    
    l_statement:=dbms_metadata.get_ddl( 'TABLE', upper(p_table_name));
    l_statement:=replace(l_statement,upper(p_table_name),upper(p_validate_table_name));
    l_statement:=replace(l_statement,'SR_SN_','SR_SNV_');
    --l_statement:='create table ' || p_validate_table_name || 
    --             ' as (select * from ' || p_table_name || ' where 1=2)';

    logger.debug(l_job_name, M_PACKAGE_NAME, l_prc_name, l_statement);
    return l_statement;
  end assemble_statement;
  
  
  procedure create_validate_table
    (p_job_name            in varchar2 default null
    ,p_table_name          in varchar2
    ,p_validate_table_name in varchar2) is

    pragma autonomous_transaction;    

    l_statement varchar2(4000);
    
  begin
   -- constraints
   -- datatype
   l_statement:=assemble_statement
      (p_job_name            => p_job_name
      ,p_table_name          => p_table_name
      ,p_validate_table_name => p_validate_table_name);
    execute immediate l_statement;
    commit;
  end;
  
  procedure validate
    (p_job_name in varchar2
    ,p_mapping  in varchar2) is
    
    l_mappings  t_mappings;
    l_mapping   t_mapping;
  begin
    l_mappings:=to_mappings(p_job_name, p_mapping);
    --for l_mapping in l_mappings loop
      --l_mapping.source
      --l_mapping.target
      null;
    --end loop;
  end;
  


end validator;
/
