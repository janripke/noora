noora
========

NoOra is a database deployment tool which can be used to automate the database deployment cycle and is designed for agile and or devops teams.
The supported database platforms are Oracle and Mysql.

# Installation
Noora currently supports Python 2.x

## Install from source using virtualenv

First, clone the repo on your machine and then install with `pip`:

```
$ svn checkout https://svn.code.sf.net/p/noora/code/trunk noora-trunk
$ mkdir noora
$ cd noora
$ virtualenv env
$ source env/bin/activate
$ cd ../noora-trunk
$ pip install .
```

## Check that the installation worked

Simply run `noora -v`.


# License
Released under the [GNU General Public License](LICENSE).
