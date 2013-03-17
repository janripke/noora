create or replace view mlog_log_v as
select id,
       logtype_code,
       job_name,
       package_name,
       method_name,
       message,
       UNIQ_SESSION_ID,
       FORMAT_ERROR_BACKTRACE,
       FORMAT_ERROR_STACK,
       FORMAT_CALL_STACK,
       CREATED_AT,
       CREATED_BY,
       UPDATED_AT,
       UPDATED_BY
from mlog$_log
where  dmltype$$='I';