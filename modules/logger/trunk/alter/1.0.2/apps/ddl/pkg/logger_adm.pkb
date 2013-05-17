create or replace package body logger_adm as
  
  M_PACKAGE_NAME                  constant varchar2(256) := lower($$plsql_unit);


  function purge
    (p_threshold_date  in date) return number is
  
  	pragma autonomous_transaction;
  
    
    l_count  number(12):=0;
    
  
  begin  
  
    delete from log where trunc(created_at) <= trunc(p_threshold_date)
    returning COUNT(*) into l_count;
    commit;
    return l_count;
  end;

  
  procedure purge
    (p_job_name       in varchar2
    ,p_threshold_date in date) is
    
    l_prc_name         varchar2(255) := 'purge';
    l_count            number(12) := 0;
    
  begin
  
    l_count := purge(p_threshold_date);          
    logger.info(p_job_name, M_PACKAGE_NAME , l_prc_name, l_count || ' log record(s) purged.');  

  end;
  
  
  procedure purge
    (p_job_name       in varchar2
    ,p_threshold_days in number) is
    
    l_prc_name         varchar2(255) := 'purge';
    l_count            number(12) := 0;
    l_threshold_date   date;
    
  begin
  
    l_threshold_date := (trunc(sysdate) - p_threshold_days);
  
    l_count := purge(l_threshold_date);          
    logger.info(p_job_name, M_PACKAGE_NAME , l_prc_name, l_count || ' log record(s) purged.');  

  end;
  
  
  procedure ins_log_archive
     (p_logtype_code in varchar2
     ,p_job_name     in varchar2 default null
     ,p_package_name in varchar2 default null
     ,p_method_name  in varchar2 default null
     ,p_message      in varchar2) is
  begin
  
    insert into log_archive 
      (id
      ,logtype_code
      ,job_name
      ,package_name
      ,method_name
      ,message
      ,uniq_session_id
      ,format_error_backtrace
      ,format_error_stack
      ,format_call_stack)
    values 
      (log_archive_s.nextval
      ,p_logtype_code
      ,p_job_name
      ,p_package_name
      ,p_method_name
      ,p_message
      ,dbms_session.unique_session_id
      ,dbms_utility.format_error_backtrace
      ,dbms_utility.format_error_stack
      ,dbms_utility.format_call_stack);      
  end;
  
  

  
end logger_adm;
/
  