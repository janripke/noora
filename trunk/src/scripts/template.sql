whenever SQLERROR exit 1
whenever OSERROR exit 2
set serveroutput off
set termout off
set feedback off
spool feedback.log
@"&1"

commit;
exit

