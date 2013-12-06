create or replace trigger log_bd
  before delete on log
  for each row
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
    ,format_call_stack
    ,created_at
    ,created_by
    ,updated_at
    ,updated_by
    ,archived_at)
  values
    (:old.id
    ,:old.logtype_code
    ,:old.job_name
    ,:old.package_name
    ,:old.method_name
    ,:old.message
    ,:old.uniq_session_id
    ,:old.format_error_backtrace
    ,:old.format_error_stack
    ,:old.format_call_stack
    ,:old.created_at
    ,:old.created_by
    ,:old.updated_at
    ,:old.updated_by
    ,sysdate);
end log_bd;
/
