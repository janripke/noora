print "creating schema $(username)"
USE $(dbf);
GO
create schema $(username) authorization $(username)