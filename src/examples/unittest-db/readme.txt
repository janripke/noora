This document contains some bootstrap info for using the unittest-db example.

Pre installation

To use the helloword-db example you need to have installed the following:
1. An oracle database, download from http://www.oracle.com/technology/software/products/database/index.html
2. An sqlplus client, download from http://www.oracle.com/technology/tech/oci/instantclient/index.html
3. Python 2.x.x, download from http://www.python.org/download/
4. Noora, download from https://sourceforge.net/projects/noora/files/

Remarks for the Python installation on Windows
1. Add the python installation folder to your PATH.

Installation of Noora

1. Download Noora, see https://sourceforge.net/projects/noora/files/
2. Extract noora.zip in a folder of choice.
3. Add the Noora folder to your PATH
4. Test the Noora installation, open a command prompt and enter the following:
   # recreate.py -v
     Noora database installer 0.0.1, recreate.py


Installation of the helloword-db example

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


Now you can use the helloworld-db example
5. Open a command prompt and enter the following:
   # cd ../noora/examples/helloword-db
   # recreate.py

If you need help or want to comment on this document sent an e-mail to janripke@gmail.com
