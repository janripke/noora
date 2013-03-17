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
  
  

  
end logger_adm;
/
  