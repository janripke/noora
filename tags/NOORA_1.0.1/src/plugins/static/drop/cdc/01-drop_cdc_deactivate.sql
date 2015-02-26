declare
  cursor c_cdc_object is
    select x.set_name
         , x.subscription_name 
         , x.status 
    from user_subscriptions x
    ;
  statement     varchar2(1024);
  M_QUOTE       varchar2(1):=chr(39);

begin
  for cdc_object in c_cdc_object loop
    if cdc_object.status <> 'N' 
      then
      statement:='begin dbms_cdc_subscribe.purge_window(subscription_name => '|| M_QUOTE || cdc_object.subscription_name || M_QUOTE||'); end;';     
      execute immediate statement;
      dbms_output.put_line(statement);
    end if;
    statement:='begin dbms_cdc_subscribe.drop_subscription(subscription_name => '|| M_QUOTE || cdc_object.subscription_name || M_QUOTE||'); end;';     
    execute immediate statement;
    dbms_output.put_line(statement);
  end loop;
end;
/
