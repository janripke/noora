create or replace package body db_logger as


  M_PACKAGE_NAME constant varchar2(256) := lower($$plsql_unit);
  
  
  procedure ins_log 
    (p_message in sys.aq$_jms_text_message) is
  
  begin
  
    insert into log 
      (id
      ,logtype_code
      ,job_name
      ,package_name
      ,method_name
      ,message
      ,uniq_session_id
      ,format_error_backtrace
      ,format_error_stack
      ,format_call_stack
      ,created_at
      ,created_by
      ,updated_at
      ,updated_by)
    values 
      (log_s.nextval
      ,p_message.get_string_property('logtype_code')
      ,p_message.get_string_property('job_name')
      ,p_message.get_string_property('package_name')
      ,p_message.get_string_property('method_name')
      ,p_message.get_string_property('message')
      ,p_message.get_string_property('uniq_session_id')
      ,p_message.get_string_property('format_error_backtrace')
      ,p_message.get_string_property('format_error_stack')
      ,p_message.get_string_property('format_call_stack')
      ,p_message.get_string_property('created_at')
      ,p_message.get_string_property('created_by')
      ,p_message.get_string_property('updated_at')
      ,p_message.get_string_property('updated_by'));

  end;
 
    
  procedure action
    (context   raw
    ,reginfo   sys.aq$_reg_info
    ,descr     sys.aq$_descriptor
    ,payload   varchar2
    ,payloadl  number) is

      l_dequeue_options    dbms_aq.dequeue_options_t;
      l_message_properties dbms_aq.message_properties_t;
      l_message_handle     raw(16);
      l_message            sys.aq$_jms_text_message;
      l_job_name           varchar2(256);
      l_prc_name           varchar2(255):='action';
      l_retry number:=0;
  begin
    
    l_dequeue_options.msgid         := descr.msg_id;
    l_dequeue_options.consumer_name := descr.consumer_name;
    l_dequeue_options.visibility    := DBMS_AQ.ON_COMMIT;

    dbms_aq.dequeue
      (queue_name         => descr.queue_name
      ,dequeue_options    => l_dequeue_options
      ,message_properties => l_message_properties
      ,payload            => l_message
      ,msgid              => l_message_handle);

	ins_log(l_message);      

    commit;
    
  exception 
  	when others then
  	  rollback;      
  end;
  
  
  procedure create_consumer
    (p_selector in varchar2 default null) is
    
    l_job_name    varchar2(256);
    l_prc_name    varchar2(100):='create_consumer';
    
  begin
    rpm_queue.create_consumer
      
      (p_package_name => M_PACKAGE_NAME
      ,p_queue        => logger.G_QUEUE
      ,p_agent        => M_PACKAGE_NAME
      ,p_selector     => p_selector);
      
	logger.info(l_job_name, M_PACKAGE_NAME, l_prc_name, 'consumer '|| M_PACKAGE_NAME || ' in queue ' || logger.G_QUEUE || ' created.' );      	
            
  end create_consumer;

end db_logger;
/
