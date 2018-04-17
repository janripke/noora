print "creating user $(username)"
use $(dbf)
create login $(username) with password = '$(password)', default_database = $(dbf)
create user $(username) with default_schema = $(username)

-- grants
grant create table to $(username);
-- :r C:\Scripts\Script1.sql

-- N'$(varMDF)'

-- sqlcmd -v varMDF="C:\dev\SAMPLE.mdf" varLDF="C:\dev\SAMPLE_log.ldf"