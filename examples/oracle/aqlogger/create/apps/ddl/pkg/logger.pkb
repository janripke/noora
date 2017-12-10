create or replace package body logger as

  QUEUE_NAME    constant varchar2(50)  := 'AQLOGGER';
  LOGTYPE_TRACE constant varchar2(50)  := 'TRACE';
  LOGTYPE_DEBUG constant varchar2(50)  := 'DEBUG';
  LOGTYPE_INFO  constant varchar2(50)  := 'INFO';
  LOGTYPE_WARN  constant varchar2(50)  := 'WARN';
  LOGTYPE_ERROR constant varchar2(50)  := 'ERROR';
  LOGTYPE_FATAL constant varchar2(50)  := 'FATAL';

  LOGTYPE 		constant varchar2(256) := app_props.get_property ( p_name => 'application.loglevel', p_default => LOGTYPE_INFO );
  
  TYPE logtype_tab IS VARRAY (6) of varchar2 (50);

  logtypes logtype_tab := logtype_tab 
   (LOGTYPE_TRACE
   ,LOGTYPE_DEBUG
   ,LOGTYPE_INFO
   ,LOGTYPE_WARN
   ,LOGTYPE_ERROR
   ,LOGTYPE_FATAL);
  
  --determine the loglevel for comparison
  function get_logtype_level 
    (p_logtype in varchar2 ) return number is
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
  function is_logging 
    (p_logtype in varchar2 ) return boolean is
  
    l_loglevel number;  
    l_clientlevel number;
    
  begin
    l_loglevel := get_logtype_level(LOGTYPE);
    l_clientlevel := get_logtype_level(p_logtype);
    if l_loglevel <= l_clientlevel
    then
      return true;
    else
      return false;
    end if;
  end;


  procedure enqueue_log
    (p_logtype_code  in varchar2
    ,p_job_name      in varchar2 default null
    ,p_package_name  in varchar2 default null
    ,p_method_name   in varchar2 default null
    ,p_message       in varchar2) is


    -- Message variables
    l_enqueue_options    dbms_aq.enqueue_options_t;
    l_message_properties dbms_aq.message_properties_t;
    l_message            sys.aq$_jms_text_message;
    l_msgid              RAW(16);
    l_sysdate            date :=sysdate;
    l_id                 number(12):=0;
    
    pragma autonomous_transaction;
    
  begin
    
    -- Set target agents
    -- l_message_properties.delay          := p_delay;
    
    l_message := sys.aq$_jms_text_message.construct;
    l_message.set_string_property('logtype_code', p_logtype_code);
    l_message.set_string_property('job_name', p_job_name);
    l_message.set_string_property('package_name', p_package_name);
    l_message.set_string_property('method_name', p_method_name);
    l_message.set_string_property('message', p_message);
    l_message.set_string_property('uniq_session_id', dbms_session.unique_session_id);
    l_message.set_string_property('format_error_backtrace', dbms_utility.format_error_backtrace);
    l_message.set_string_property('format_error_stack', dbms_utility.format_error_stack);
    l_message.set_string_property('format_call_stack', dbms_utility.format_call_stack);
    l_message.set_string_property('created_at', l_sysdate);
    l_message.set_string_property('created_by', user);
    l_message.set_string_property('updated_at', l_sysdate);
    l_message.set_string_property('updated_by', user);
    dbms_aq.enqueue
      (QUEUE_NAME
      ,l_enqueue_options
      ,l_message_properties
      ,l_message
      ,l_msgid);
      
    commit;      
   
  end enqueue_log;


  procedure trace 
    (p_job_name     in varchar2 default null
    ,p_package_name in varchar2 default null
    ,p_method_name  in varchar2 default null
    ,p_message      in varchar2 ) is
  begin
    if is_logging ( p_logtype => LOGTYPE_TRACE )
    then
      enqueue_log 
        (p_logtype_code => LOGTYPE_TRACE
        ,p_job_name     => p_job_name
        ,p_package_name => p_package_name
        ,p_method_name  => p_method_name
        ,p_message      => p_message);
    end if;
  end;

  procedure debug
    (p_job_name     in varchar2 default null
    ,p_package_name in varchar2 default null
    ,p_method_name  in varchar2 default null
    ,p_message      in varchar2 ) is
  begin
    if is_logging ( p_logtype => LOGTYPE_DEBUG )
    then
      enqueue_log 
        (p_logtype_code => LOGTYPE_DEBUG
        ,p_job_name     => p_job_name
        ,p_package_name => p_package_name
        ,p_method_name  => p_method_name
        ,p_message      => p_message);
    end if;
  end;

  procedure info
    (p_job_name     in varchar2 default null
    ,p_package_name in varchar2 default null
    ,p_method_name  in varchar2 default null
    ,p_message      in varchar2 ) is
  begin
    if is_logging ( p_logtype => LOGTYPE_INFO )
    then
      enqueue_log 
        (p_logtype_code => LOGTYPE_INFO
        ,p_job_name     => p_job_name
        ,p_package_name => p_package_name
        ,p_method_name  => p_method_name
        ,p_message      => p_message);
    end if;
  end;

  procedure warn 
    (p_job_name     in varchar2 default null
    ,p_package_name in varchar2 default null
    ,p_method_name  in varchar2 default null
    ,p_message      in varchar2 ) is
  begin
    if is_logging ( p_logtype => LOGTYPE_WARN )
    then
      enqueue_log 
      	(p_logtype_code => LOGTYPE_WARN
        ,p_job_name     => p_job_name
        ,p_package_name => p_package_name
        ,p_method_name  => p_method_name
        ,p_message      => p_message);
    end if;
  end;

  procedure error
    (p_job_name     in varchar2 default null
    ,p_package_name in varchar2 default null
    ,p_method_name  in varchar2 default null
    ,p_message      in varchar2 ) is
  begin
    if is_logging ( p_logtype => LOGTYPE_ERROR )
    then
      enqueue_log 
        (p_logtype_code => LOGTYPE_ERROR
        ,p_job_name     => p_job_name
        ,p_package_name => p_package_name
        ,p_method_name  => p_method_name
        ,p_message      => p_message);
    end if;
  end;

  procedure fatal 
    (p_job_name     in varchar2 default null
    ,p_package_name in varchar2 default null
    ,p_method_name  in varchar2 default null
    ,p_message      in varchar2 ) is
  begin
    if is_logging ( p_logtype => LOGTYPE_FATAL)
    then
      enqueue_log 
        (p_logtype_code => LOGTYPE_FATAL
        ,p_job_name     => p_job_name
        ,p_package_name => p_package_name
        ,p_method_name  => p_method_name
        ,p_message      => p_message);
    end if;
  end;
  

  
end logger;
/
