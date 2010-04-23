whenever SQLERROR exit 1
whenever OSERROR exit 2
define SCRIPT=&1
set serveroutput off
set termout off
set feedback off
spool feedback.log
@&SCRIPT

commit;
exit

