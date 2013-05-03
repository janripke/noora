whenever SQLERROR exit 1
whenever OSERROR exit 2
set serveroutput off
set termout off
set feedback off
spool install.log append
spool feedback.log
prompt "&1"
@@"&1"

commit;
spool off
exit
