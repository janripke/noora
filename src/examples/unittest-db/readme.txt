This document contains some info on using the unittest-db example.

Pre installation

To use the unittest-db example you need to have installed the following:
1. An oracle database, download it from http://www.oracle.com/technology/software/products/database/index.html
2. An sqlplus client, download it from http://www.oracle.com/technology/tech/oci/instantclient/index.html
3. Python 2.x.x, download it from http://www.python.org/download/
4. Noora, download it from https://sourceforge.net/projects/noora/files/

Remarks for the Python installation on Windows
1. Add the python installation folder to your PATH.


Installation of Noora

1. Download Noora, see https://sourceforge.net/projects/noora/files/
2. Extract noora.zip in a folder of choice.
3. Add the Noora folder to your PATH
4. Test the Noora installation, open a command prompt and enter the following:
   # recreate.py -v
     Noora database installer 0.0.1, recreate.py


Installation of the unittest-db example

1. Create the tablespaces APPDAT and APPIDX in your Oracle database.
   An example can be found in the create_tablespaces.sql file.
   To use this script you need to connect as sysdba to your database and 
   change the location of the datafile in the script.
   # sqlplus SYS/SYS@orcl as sysdba
   SQL> @ create_tablespaces.sql
   SQL> exit;
2. Create the user apps with password apps in your Oracle database.
   An example can be found in the create_user_apps.sql file.
   To use this script you need to connect as sysdba to your database.
   # sqlplus SYS/SYS@orcl as sysdba
   SQL> @ create_user_apps.sql
   SQL> exit;
3. Give the user apps the necessary grants. 
4. Change the DEFAULT_ORACLE_SID value in the config.py to the oracle sid of your database.


Creating the unittest-db example:
1. Open a command prompt and enter the following:
   # cd ../noora/examples/unittest-db
   # recreate.py


Running the unit test example:
1. Open a command prompt and enter the following:
   # cd ../noora/examples/unittest-db
   # unittest.py
     executing unit tests for schema apps
     declare
     *
     ERROR at line 1:
     ORA-20002: ORA-06512: at "APPS.UT_ASSERT", line 27 
     ORA-06512: at "APPS.UT_APP_PROP", line 45 
     ORA-06512: at line 1 
     ORA-06512: at "APPS.UT_RUN", line 73 
     ORA-06512: at "APPS.UT_RUN", line 84 
     ORA-20001: [t_get_property], invalid property value: test.code <> test1.code 
     ORA-06512: at "APPS.UT_RUN", line 96 
     ORA-06512: at line 1 
     ORA-06512: at line 18
     
unittest.py will execute all the unit tests of the schema apps.
Considered as unit test's are package that start with ut_.
Excluded are the packages ut_assert en ut_run. ut_assert is used to 
create assertions in your unit tests. 
ut_run is a helper to run your unit tests.
In this example i wrote one unit test. It is called ut_app_prop.
I made an error in this unit test, on line 45. It is to show you
what happens when a unit test fails.


If you need help or want to comment on this document,
sent an e-mail to janripke@gmail.com
