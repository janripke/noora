set serveroutput on
declare
  cursor c_user_objects is
    select object_name
    from user_objects
    where object_type='MATERIALIZED VIEW';

  cursor c_user_mview_logs is
    select master
    from user_mview_logs;

  statement	varchar2(1024);
  M_DQUOTE      varchar2(1):='"';


begin
  for user_object in c_user_objects loop
    statement:='DROP MATERIALIZED VIEW ' || M_DQUOTE || user_object.object_name || M_DQUOTE;
    execute immediate statement;
  end loop;

  for user_mview_log in c_user_mview_logs loop
    statement:='DROP MATERIALIZED VIEW LOG ON ' || M_DQUOTE || user_mview_log.master || M_DQUOTE;
    execute immediate statement;
  end loop;

end;
/
set serveroutput off
