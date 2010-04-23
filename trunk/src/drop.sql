whenever SQLERROR exit 1
whenever OSERROR exit 2
set serveroutput off
set termout off
spool feedback.log
define SCRIPT=&1
@&SCRIPT

commit;
exit

