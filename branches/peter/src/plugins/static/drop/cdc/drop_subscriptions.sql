set serveroutput on
declare
  cursor c_user_subscriptions is
    select subscription_name 
    from user_subscriptions
    ; 

  statement	varchar2(1024);
  subscription_name    varchar2(256);
  constraint_name varchar2(256);
  M_DQUOTE      varchar2(1):='''';
  
begin
  for user_subscription in c_user_subscriptions loop
    subscription_name:=user_subscription.subscription_name;
    statement:='BEGIN DBMS_CDC_PUBLISH.DROP_SUBSCRIPTION(' || M_DQUOTE || subscription_name || M_DQUOTE || '); END;';  
    dbms_output.put_line(statement);
    execute immediate statement;
  end loop;
end;
/
set serveroutput off
