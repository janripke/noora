print "creating users..."
:setvar dbf "elsevierdb"
:setvar username "apps"
:setvar password "apps"
:r create_user.sql
:r create_schema.sql