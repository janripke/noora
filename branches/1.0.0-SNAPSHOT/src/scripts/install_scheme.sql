whenever SQLERROR exit 1
whenever OSERROR exit 2
set serveroutput off
set termout on
set echo       off
set feedback   off
set serveroutput on size unlimited
spool feedback.log
define ENVIRONMENT=&1

@@"<install>"

commit;
exit

