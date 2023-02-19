# ![noora logo](https://a.fsdn.com/allura/p/noora/icon)

# technical backlog
* remove File classes, can be replaced by pathlib functionality.
* create a deploy plugin for mssql and mysql
* create a build plugin for postgresql and mssql, using the in mysql as a template.
* create a deploy plugin for mssql and mysql
* replace the version class with a version dataclass
* change .format string to formatted strings
* create and test a python application, using actions on github

  https://github.com/janripke/noora/actions/new

* publish a python package to PyPI on release, using actions on github
  
  https://github.com/janripke/noora/actions/new

* use pyproject.toml in favour of setup.py, which is marked as deprecated by pip.

  https://setuptools.pypa.io/en/latest/userguide/pyproject_config.html
  
  https://pip.pypa.io/en/stable/reference/build-system/pyproject-toml/