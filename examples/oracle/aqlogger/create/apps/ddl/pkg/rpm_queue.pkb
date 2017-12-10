create or replace package body aq_helper as

  M_PACKAGE_NAME   constant varchar2(256):= lower($$plsql_unit);

  procedure create_agent
    (p_agent in user_aq_agent_privs.agent_name%type) is
    
      l_job_name    varchar2(256);
      l_prc_name    varchar2(100):='create_agent';
      
  begin
    dbms_aqadm.create_aq_agent(p_agent);
    logger.info(l_job_name, M_PACKAGE_NAME, l_prc_name, 'agent ' || p_agent || ' created.');
      
    -- This procedure grants an Oracle Streams AQ Internet agent 
    -- the privileges of a specific database user.
    dbms_aqadm.enable_db_access(p_agent, USER);
    logger.info(l_job_name, M_PACKAGE_NAME, l_prc_name, 'access of agent ' || p_agent || ' to user ' || USER || ' granted.');
  end;
   

  procedure drop_agent
    (p_agent in user_aq_agent_privs.agent_name%type) is
     
    l_job_name    varchar2(256);
    l_prc_name    varchar2(100):='drop_agent';
     
  begin
    dbms_aqadm.drop_aq_agent(p_agent);
    logger.debug(l_job_name, M_PACKAGE_NAME, l_prc_name, 'agent ' || p_agent || ' dropped.');
  end;


  procedure subscribe
    (p_queue      in varchar2
    ,p_agent      in user_aq_agent_privs.agent_name%type
    ,p_selector   in varchar2 DEFAULT NULL) is
    
    l_job_name    varchar2(256);
    l_prc_name    varchar2(100):='subscribe';
  
  begin
    dbms_aqadm.add_subscriber
      (queue_name => p_queue
      ,subscriber => sys.aq$_agent(p_agent, NULL, NULL)
      ,rule       => p_selector);
      
    logger.info(l_job_name, M_PACKAGE_NAME, l_prc_name, 'agent ' || p_agent ||  ' subscribed to queue ' || p_queue || ' using selector ' || p_selector);
        
  end;
  
  
  function is_subscriber
  	(p_queue in varchar2
  	,p_agent in varchar2) return boolean is
  	
  begin
  
    select count(0) 
    into   l_count 
    from   user_queue_subscribers
    where  queue_name    = upper(p_queue)
    and    consumer_name = upper(p_agent);
    
    if l_count > 0 then
      return true;
    end if;
    
    return false;
  
  end;

  
  procedure unsubscribe
    (p_queue      in varchar2
    ,p_agent      in varchar2) is
    
    l_job_name    varchar2(256);
    l_prc_name    varchar2(100):='unsubscribe';
  
  begin
    dbms_aqadm.remove_subscriber
      (queue_name => p_queue
      ,subscriber => sys.aq$_agent(p_agent, NULL, NULL) );

    logger.info(l_job_name, M_PACKAGE_NAME, l_prc_name, 'agent ' || p_agent ||  ' subscribed to queue ' || p_queue || ' unsubscribed.');    
  end;


  procedure register
    (p_package_name in varchar2
    ,p_queue        in varchar2
    ,p_agent        in user_aq_agent_privs.agent_name%type) is
    
    l_job_name    varchar2(256);
    l_prc_name    varchar2(100):='register';
  
  begin
    dbms_aq.register
      (sys.aq$_reg_info_list(sys.aq$_reg_info(p_queue||':'||p_agent
                                                            , dbms_aq.namespace_aq, 'plsql://'||p_package_name||'.action'
                                                            , HEXTORAW('FF')))
                                                            ,1);
    logger.info(l_job_name, M_PACKAGE_NAME, l_prc_name, 'package ' || p_package || ' registered to ' || agent ' || p_agent ||  ' subscribed to queue ' || p_queue);
    
    
  end;

  
  procedure unregister
    (p_package_name in varchar2
    ,p_queue        in varchar2
    ,p_agent        in user_aq_agent_privs.agent_name%type) is
      
    l_job_name    varchar2(256);
    l_prc_name    varchar2(100):='unregister';
    
  begin
    dbms_aq.unregister
      (sys.aq$_reg_info_list(sys.aq$_reg_info(
                                               p_queue||':'||p_agent
                                             , dbms_aq.namespace_aq
                                             , 'plsql://'||p_package_name||'.action'
                                             , HEXTORAW('FF'))
                                           )
                        ,1);
                        
    logger.info(l_job_name, M_PACKAGE_NAME, l_prc_name, 'package ' || p_package || ' registered to ' || agent ' || p_agent ||  ' subscribed to queue ' || p_queue || ' unregistered.');
  end;

  procedure create_consumer
    (p_package_name in varchar2
    ,p_queue        in varchar2
    ,p_agent        in user_aq_agent_privs.agent_name%type
    ,p_selector     in varchar2) is
                            
    l_job_name    varchar2(256);
    l_prc_name    varchar2(100):='create_consumer';
 
  begin    
  
    -- Create agent       
    create_agent
      (p_agent => p_agent);
  
    -- Subscribe
    subscribe
      (p_queue    => p_queue
      ,p_agent    => p_agent
      ,p_selector => p_selector);
    
    -- Register
    register
      (p_package_name => p_package_name
      ,p_queue        => p_queue
      ,p_agent        => p_agent);
      
  end;


  procedure remove_consumer
    (p_package_name in varchar2
    ,p_queue        in varchar2
    ,p_agent        in user_aq_agent_privs.agent_name%type) is
    
    
    l_job_name    varchar2(256);
    l_prc_name    varchar2(100):='remove_consumer';
  begin
       
    -- Unsubscribe
    unsubscribe
      (p_queue => p_queue
      ,p_agent => p_agent);

     -- Unregister
     unregister
       (p_package_name => p_package_name
       ,p_queue        => p_queue
       ,p_agent        => p_agent);
     
     --Drop agent
     drop_agent
       (p_agent => p_agent);
  end;
  
end aq_helper;
/
