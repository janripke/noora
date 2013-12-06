/*
 *   Name         : create_owner_user.sql
 *   Purpose      : Create a user which is able to create objects in the NUON databases
 *                  The rights of this user are the same as with Asp4All
 *   Date         : 24-08-2011
 *   Author       : Frans Jacobs
 *   Remarks      : Script should be run as sys
*/

define SCHEMA_OWNER = &1
define SCHEMA_PASSWD = &2

define TS_DEFAULT = TS_DATA
--drop user &SCHEMA_OWNER cascade;

prompt ##############################################
prompt Creating user &SCHEMA_OWNER.
prompt ##############################################

create user &SCHEMA_OWNER
       identified by &SCHEMA_PASSWD
       default tablespace &TS_DEFAULT;

grant connect, resource to &SCHEMA_OWNER;
grant create any directory to &SCHEMA_OWNER;
grant create job to &SCHEMA_OWNER;
grant create external job to &SCHEMA_OWNER;
grant create synonym to &SCHEMA_OWNER;
grant create view to &SCHEMA_OWNER;
grant create materialized view to &SCHEMA_OWNER;

grant create trigger to &SCHEMA_OWNER;

grant create sequence to &SCHEMA_OWNER;
grant create database link to &SCHEMA_OWNER;

grant create any table to &SCHEMA_OWNER;
grant create any sequence to &SCHEMA_OWNER;

grant execute on dbms_crypto to &SCHEMA_OWNER;
grant execute on dbms_lock to &SCHEMA_OWNER;
grant execute ON dbms_lock TO &SCHEMA_OWNER;

prompt ###############################################
prompt Grant &SCHEMA_OWNER on some system v$ views...
prompt ###############################################

grant select on sys.v_$instance to &SCHEMA_OWNER;
grant select on sys.v_$lock to &SCHEMA_OWNER;
grant select on sys.v_$nls_parameters to &SCHEMA_OWNER;
grant select on sys.v_$open_cursor to &SCHEMA_OWNER;
grant select on sys.v_$parameter to &SCHEMA_OWNER;
grant select on sys.v_$session to &SCHEMA_OWNER;
grant select on sys.v_$session_longops to &SCHEMA_OWNER;
grant select on sys.v_$sesstat to &SCHEMA_OWNER;
grant select on sys.v_$sql to &SCHEMA_OWNER;
grant select on sys.v_$sqltext_with_newlines to &SCHEMA_OWNER;
grant select on sys.v_$statname to &SCHEMA_OWNER;
grant select on sys.v_$transaction to &SCHEMA_OWNER;

GRANT JAVAUSERPRIV TO &SCHEMA_OWNER;
GRANT JAVA_ADMIN TO &SCHEMA_OWNER;
GRANT JAVA_DEPLOY TO &SCHEMA_OWNER;
GRANT JAVASYSPRIV TO &SCHEMA_OWNER;
GRANT JAVAIDPRIV TO &SCHEMA_OWNER;



--Necessary for Change Data Capture (Oracle Streams)
GRANT EXECUTE_CATALOG_ROLE to &SCHEMA_OWNER;
GRANT SELECT_CATALOG_ROLE to &SCHEMA_OWNER;

-- grants to run java based stored procedures
/*
BEGIN
DBMS_JAVA.GRANT_PERMISSION('DBA_JAVA'
                           ,'SYS:java.io.FilePermission'
                           ,'<<ALL FILES>>'
                           ,'read,write,execute');
DBMS_JAVA.GRANT_PERMISSION('DBA_JAVA'
                           ,'SYS:java.lang.RuntimePermission'
                           ,'readFileDescriptor'
                           ,'');
DBMS_JAVA.GRANT_PERMISSION('DBA_JAVA'
                           ,'SYS:java.lang.RuntimePermission'
                           ,'readFileDescriptor'
                           ,'writeFileDescriptor');
END;
/
*/

GRANT aq_administrator_role TO &SCHEMA_OWNER;
GRANT aq_user_role TO &SCHEMA_OWNER;

GRANT EXECUTE ON dbms_aq TO &SCHEMA_OWNER;
GRANT EXECUTE ON dbms_aqadm TO &SCHEMA_OWNER;
GRANT EXECUTE ANY PROCEDURE TO &SCHEMA_OWNER;
EXECUTE dbms_aqadm.grant_system_privilege('ENQUEUE_ANY','&SCHEMA_OWNER',TRUE);
EXECUTE dbms_aqadm.grant_system_privilege('DEQUEUE_ANY','&SCHEMA_OWNER',TRUE);
EXECUTE dbms_aqadm.grant_type_access('&SCHEMA_OWNER');

