create or replace package body logger as

  LOGTYPE_TRACE constant varchar2(50) := 'TRACE';
  LOGTYPE_DEBUG constant varchar2(50) := 'DEBUG';
  LOGTYPE_INFO  constant varchar2(50) := 'INFO';
  LOGTYPE_WARN  constant varchar2(50) := 'WARN';
  LOGTYPE_ERROR constant varchar2(50) := 'ERROR';
  LOGTYPE_FATAL constant varchar2(50) := 'FATAL';

  LOGTYPE constant varchar2 (256) := app_props.get_property ( p_name => 'application.loglevel', p_default => LOGTYPE_INFO );
  
  TYPE logtype_tab IS VARRAY (6) of varchar2 (50);

  logtypes logtype_tab := logtype_tab ( LOGTYPE_TRACE
                                      , LOGTYPE_DEBUG
                                      , LOGTYPE_INFO
                                      , LOGTYPE_WARN
                                      , LOGTYPE_ERROR
                                      , LOGTYPE_FATAL );
  
  --determine the loglevel for comparison
  function get_logtype_level ( p_logtype in varchar2 )
    return number
  is
  begin
    for i in 1 ..6
    loop
      if p_logtype = logtypes ( i )
      then
        return i;
      end if;
    end
    loop;
    return 0;
  end;
   
  --determine whether 'we' must log...
  function is_logging ( p_logtype in varchar2 )
    return boolean
  is
    l_loglevel number;
    l_clientlevel number;
  begin
    l_loglevel := get_logtype_level ( LOGTYPE );
    l_clientlevel := get_logtype_level ( p_logtype );
    if l_loglevel <= l_clientlevel
    then
      return true;
    else
      return false;
    end if;

  end;

  --Main logger procedure, which does the insert into the log table...
  procedure ins_log ( p_logtype_code in varchar2
                    , p_job_name in varchar2 default null
                    , p_package_name in varchar2 default null
                    , p_method_name in varchar2 default null
                    , p_message in varchar2 )
  is
    pragma autonomous_transaction;
  begin
    insert into log ( id
                    , logtype_code
                    , job_name
                    , package_name
                    , method_name
                    , message
                    , uniq_session_id
                    , format_error_backtrace
                    , format_error_stack
                    , format_call_stack)
    values ( log_s.nextval
           , p_logtype_code
           , p_job_name
           , p_package_name
           , p_method_name
           , p_message
           , dbms_session.unique_session_id
           , dbms_utility.format_error_backtrace
           , dbms_utility.format_error_stack
           , dbms_utility.format_call_stack);
    commit;
  end;

  procedure trace ( p_job_name in varchar2 default null
                  , p_package_name in varchar2 default null
                  , p_method_name in varchar2 default null
                  , p_message in varchar2 )
  is
  begin
    if is_logging ( p_logtype => LOGTYPE_TRACE )
    then
      ins_log ( p_logtype_code => LOGTYPE_TRACE
              , p_job_name => p_job_name
              , p_package_name => p_package_name
              , p_method_name => p_method_name
              , p_message => p_message);
    end if;
  end;

  procedure debug ( p_job_name in varchar2 default null
                  , p_package_name in varchar2 default null
                  , p_method_name in varchar2 default null
                  , p_message in varchar2 )
  is
  begin
    if is_logging ( p_logtype => LOGTYPE_DEBUG )
    then
      ins_log ( p_logtype_code => LOGTYPE_DEBUG
              , p_job_name => p_job_name
              , p_package_name => p_package_name
              , p_method_name => p_method_name
              , p_message => p_message);
    end if;
  end;

  procedure info ( p_job_name in varchar2 default null
                  , p_package_name in varchar2 default null
                  , p_method_name in varchar2 default null
                  , p_message in varchar2 )
  is
  begin
    if is_logging ( p_logtype => LOGTYPE_INFO )
    then
      ins_log ( p_logtype_code => LOGTYPE_INFO
              , p_job_name => p_job_name
              , p_package_name => p_package_name
              , p_method_name => p_method_name
              , p_message => p_message);
    end if;
  end;

  procedure warn ( p_job_name in varchar2 default null
                  , p_package_name in varchar2 default null
                  , p_method_name in varchar2 default null
                  , p_message in varchar2 )
  is
  begin
    if is_logging ( p_logtype => LOGTYPE_WARN )
    then
      ins_log ( p_logtype_code => LOGTYPE_WARN
              , p_job_name => p_job_name
              , p_package_name => p_package_name
              , p_method_name => p_method_name
              , p_message => p_message);
    end if;
  end;

  procedure error ( p_job_name in varchar2 default null
                  , p_package_name in varchar2 default null
                  , p_method_name in varchar2 default null
                  , p_message in varchar2 )
  is
  begin
    if is_logging ( p_logtype => LOGTYPE_ERROR )
    then
      ins_log ( p_logtype_code => LOGTYPE_ERROR
              , p_job_name => p_job_name
              , p_package_name => p_package_name
              , p_method_name => p_method_name
              , p_message => p_message);
    end if;
  end;

  procedure fatal ( p_job_name in varchar2 default null
                  , p_package_name in varchar2 default null
                  , p_method_name in varchar2 default null
                  , p_message in varchar2 )
  is
  begin
    if is_logging ( p_logtype => LOGTYPE_FATAL)
    then
      ins_log ( p_logtype_code => LOGTYPE_FATAL
              , p_job_name => p_job_name
              , p_package_name => p_package_name
              , p_method_name => p_method_name
              , p_message => p_message);
    end if;
  end;
end logger;
/
