declare
  cursor c_user_subscriptions is
    select subscription_name
    from   user_subscriptions;
begin
  for rec in c_user_subscriptions
  loop
    execute immediate 'begin dbms_cdc_publish.drop_change_table(:1); end;'
      using rec.subscription_name;
  end loop;
exception
  when others then
    null;
end;
/
