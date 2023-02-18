from unittest.mock import MagicMock, patch

from click.testing import CliRunner

from noora.plugins.postgresql.drop import cli as drop
from noora.plugins.postgresql.create import cli as create
from noora.plugins.postgresql.update import cli as update
from noora.plugins.postgresql.recreate import cli as recreate
from noora.plugins.postgresql.deploy import cli as deploy
from noora.system.Properties import Properties


@patch("noora.shell.Shell.Shell.execute")
def test_drop_pass(command: MagicMock):
    """
    This test passes when the drop scripts are executed.
    """
    # set the SQL output, an empty string means the SQL statement is successfully executed
    command.return_value = ""

    # read the properties from myproject.json, normally handled by mynoora_cli
    props = Properties()

    runner = CliRunner()
    result = runner.invoke(drop, obj=props)

    print(result.output)
    assert result.exit_code == 0
    assert "database 'acme' dropped" in result.output


@patch("noora.shell.Shell.Shell.execute")
def test_drop_connection_string_pass(command: MagicMock):
    """
    This test passes when the drop scripts are executed.
    """
    # set the SQL output, an empty string means the SQL statement is successfully executed
    command.return_value = ""

    # read the properties from myproject.json, normally handled by mynoora_cli
    props = Properties()

    runner = CliRunner()
    result = runner.invoke(drop, obj=props, args=["--connection-string", "host=localhost,port=5432,database=acme,username=acme_owner,password=acme_owner"])

    print(f"exception={result.output}")
    assert result.exit_code == 0
    assert "database 'acme' dropped" in result.output


@patch("noora.shell.Shell.Shell.execute")
def test_drop_unknown_host_fail(command: MagicMock):
    """
    This test passes when a PluginException is raised, with the message
    Host unknown_host not in list of valid hosts for this project.
    """
    # set the SQL output, an empty string means the SQL statement is successfully executed
    command.return_value = ""

    # read the properties from myproject.json, normally handled by mynoora_cli
    props = Properties()

    runner = CliRunner()
    result = runner.invoke(drop, obj=props, args=["--host", "unknown_host"])

    print(f"exception={result.exception}")
    assert result.exit_code == 1
    assert "Host unknown_host not in list of valid hosts for this project" in result.exception.__str__()


@patch("noora.shell.Shell.Shell.execute")
def test_drop_host_mismatch_fail(command: MagicMock):
    """
    This test passes when a PluginException is raised, with the message
    Host 'localhost' not present in connection-string.
    """
    # set the SQL output, an empty string means the SQL statement is successfully executed
    command.return_value = ""

    # read the properties from myproject.json, normally handled by mynoora_cli
    props = Properties()

    runner = CliRunner()
    result = runner.invoke(drop, obj=props, args=["--connection-string", "host=unknown_host,port=5432,database=acme,username=acme_owner,password=acme_owner"])

    print(f"exception={result.exception}")
    assert result.exit_code == 1
    assert "Host 'localhost' not present in connection-string" in result.exception.__str__()


@patch("noora.shell.Shell.Shell.execute")
def test_create_pass(command: MagicMock):
    """
    This test passes when the create scripts are executed.
    """
    # set the SQL output, an empty string means the SQL statement is successfully executed
    command.return_value = ""

    # read the properties from myproject.json, normally handled by mynoora_cli
    props = Properties()

    runner = CliRunner()
    result = runner.invoke(create, obj=props)

    print(f"output={result.output}")
    assert result.exit_code == 0
    assert "database 'acme' created." in result.output


@patch("noora.shell.Shell.Shell.execute")
def test_create_unknown_host_fail(command: MagicMock):
    """
    This test passes when a PluginException is raised, with the message
    Host unknown_host not in list of valid hosts for this project.
    """
    # set the SQL output, an empty string means the SQL statement is successfully executed
    command.return_value = ""

    # read the properties from myproject.json, normally handled by mynoora_cli
    props = Properties()

    runner = CliRunner()
    result = runner.invoke(create, obj=props, args=["--host", "unknown_host"])

    print(f"exception={result.exception}")
    assert result.exit_code == 1
    assert "Host unknown_host not in list of valid hosts for this project" in result.exception.__str__()


@patch("noora.shell.Shell.Shell.execute")
def test_create_host_mismatch_fail(command: MagicMock):
    """
    This test passes when a PluginException is raised, with the message
    Host 'localhost' not present in connection-string.
    """
    # set the SQL output, an empty string means the SQL statement is successfully executed
    command.return_value = ""

    # read the properties from myproject.json, normally handled by mynoora_cli
    props = Properties()

    runner = CliRunner()
    result = runner.invoke(create, obj=props, args=["--connection-string", "host=unknown_host,port=5432,database=acme,username=acme_owner,password=acme_owner"])

    print(f"exception={result.exception}")
    assert result.exit_code == 1
    assert "Host 'localhost' not present in connection-string" in result.exception.__str__()


@patch("noora.shell.Shell.Shell.execute")
def test_update_pass(command: MagicMock):
    """
    This test passes when the update scripts for version 1.0.1 are executed.
    """
    # set the SQL output, an empty string means the SQL statement is successfully executed
    command.return_value = ""

    # read the properties from myproject.json, normally handled by mynoora_cli
    props = Properties()

    runner = CliRunner()
    result = runner.invoke(update, args=["--version", "1.0.1"], obj=props)

    print(result.output)
    assert result.exit_code == 0
    assert "database 'acme' updated" in result.output


@patch("noora.shell.Shell.Shell.execute")
def test_update_unknown_host_fail(command: MagicMock):
    """
    This test passes when a PluginException is raised, with the message
    Host unknown_host not in list of valid hosts for this project.
    """
    # set the SQL output, an empty string means the SQL statement is successfully executed
    command.return_value = ""

    # read the properties from myproject.json, normally handled by mynoora_cli
    props = Properties()

    runner = CliRunner()
    result = runner.invoke(update, obj=props, args=["--host", "unknown_host", "--version", "1.0.1"])

    print(f"exception={result.exception}")
    assert result.exit_code == 1
    assert "Host unknown_host not in list of valid hosts for this project" in result.exception.__str__()


@patch("noora.shell.Shell.Shell.execute")
def test_update_host_mismatch_fail(command: MagicMock):
    """
    This test passes when a PluginException is raised, with the message
    Host 'localhost' not present in connection-string.
    """
    # set the SQL output, an empty string means the SQL statement is successfully executed
    command.return_value = ""

    # read the properties from myproject.json, normally handled by mynoora_cli
    props = Properties()

    runner = CliRunner()
    result = runner.invoke(update, obj=props, args=["--version", "1.0.1", "--connection-string", "host=unknown_host,port=5432,database=acme,username=acme_owner,password=acme_owner"])

    print(f"exception={result.exception}")
    assert result.exit_code == 1
    assert "Host 'localhost' not present in connection-string" in result.exception.__str__()


@patch("noora.shell.Shell.Shell.execute")
def test_recreate_pass(command: MagicMock):
    """
    This test passes when the drop, create and update parts are executed.
    """
    # set the SQL output, an empty string means the SQL statement is successfully executed
    command.return_value = ""

    # read the properties from myproject.json, normally handled by mynoora_cli
    props = Properties()

    runner = CliRunner()
    result = runner.invoke(recreate, obj=props)

    print(result.output)
    assert result.exit_code == 0
    assert "database 'acme' dropped" in result.output
    assert "database 'acme' created." in result.output
    assert "database 'acme' updated" in result.output


@patch("noora.shell.Shell.Shell.execute")
def test_recreate_connection_string_pass(command: MagicMock):
    """
    This test passes when the drop, create and update parts are executed.
    """
    # set the SQL output, an empty string means the SQL statement is successfully executed
    command.return_value = ""

    # read the properties from myproject.json, normally handled by mynoora_cli
    props = Properties()

    runner = CliRunner()
    result = runner.invoke(recreate, obj=props, args=["--host", "localhost", "--connection-string", "host=localhost,port=5432,database=acme,username=acme_owner,password=acme_owner"])

    print(result.output)
    assert result.exit_code == 0
    assert "database 'acme' dropped" in result.output
    assert "database 'acme' created." in result.output
    assert "database 'acme' updated" in result.output


@patch("noora.shell.Shell.Shell.execute")
def test_recreate_unknown_host_fail(command: MagicMock):
    """
    This test passes when a PluginException is raised, with the message
    Host unknown_host not in list of valid hosts for this project.
    """

    # set the SQL output, an empty string means the SQL statement is successfully executed
    command.return_value = ""

    # read the properties from myproject.json, normally handled by mynoora_cli
    props = Properties()

    runner = CliRunner()
    result = runner.invoke(recreate, obj=props, args=["--host", "unknown_host"])

    print(f"exception={result.exception}")
    assert result.exit_code == 1
    assert "Host unknown_host not in list of valid hosts for this project" in result.exception.__str__()


@patch("noora.shell.Shell.Shell.execute")
def test_recreate_host_mismatch_fail(command: MagicMock):
    """
    This test passes when a PluginException is raised, with the message
    Host 'localhost' not present in connection-string.
    """

    # set the SQL output, an empty string means the SQL statement is successfully executed
    command.return_value = ""

    # read the properties from myproject.json, normally handled by mynoora_cli
    props = Properties()

    runner = CliRunner()
    result = runner.invoke(recreate, obj=props, args=["--connection-string", "host=unknown_host,port=5432,database=acme,username=acme_owner,password=acme_owner"])

    print(f"exception={result.exception}")
    assert result.exit_code == 1
    assert "Host 'localhost' not present in connection-string" in result.exception.__str__()


@patch("noora.shell.Shell.Shell.execute")
def test_deploy_pass(command: MagicMock):
    """
    This test passes when both the create and update parts are executed.
    """

    # set the SQL output, an empty string means the SQL statement is successfully executed
    command.return_value = ""

    # read the properties from myproject.json, normally handled by mynoora_cli
    props = Properties()

    runner = CliRunner()
    result = runner.invoke(deploy, obj=props)

    print(result.output)
    assert result.exit_code == 0
    assert "database 'acme' created." in result.output
    assert "database 'acme' updated" in result.output


@patch("noora.shell.Shell.Shell.execute")
def test_deploy_create_only_pass(command: MagicMock):
    """
    This test passes when the create part and only the create part is executed.
    """

    # set the SQL output, an empty string means the SQL statement is successfully executed
    command.return_value = ""

    # read the properties from myproject.json, normally handled by mynoora_cli
    props = Properties()

    runner = CliRunner()
    result = runner.invoke(deploy, obj=props, args=["--version", "1.0.0"])

    print(result.output)
    assert result.exit_code == 0
    assert "database 'acme' created" in result.output
    assert "database 'acme' updated" not in result.output


@patch("noora.shell.Shell.Shell.execute")
def test_deploy_unknown_host_fail(command: MagicMock):
    """
    This test passes when a PluginException is raised, with the message
    Host unknown_host not in list of valid hosts for this project.
    """

    # set the SQL output, an empty string means the SQL statement is successfully executed
    command.return_value = ""

    # read the properties from myproject.json, normally handled by mynoora_cli
    props = Properties()

    runner = CliRunner()
    result = runner.invoke(deploy, obj=props, args=["--host", "unknown_host"])

    print(f"exception={result.exception}")
    assert result.exit_code == 1
    assert "Host unknown_host not in list of valid hosts for this project" in result.exception.__str__()


@patch("noora.shell.Shell.Shell.execute")
def test_deploy_no_host_fail(command: MagicMock):
    """
    This test passes when a PluginException is raised, with the message
    no host was given.
    """

    # set the SQL output, an empty string means the SQL statement is successfully executed
    command.return_value = ""

    # read the properties from myproject.json, normally handled by mynoora_cli
    props = Properties()

    runner = CliRunner()
    result = runner.invoke(deploy, obj=props, args=["--host", ""])

    print(f"exception={result.exception}")
    assert result.exit_code == 1
    assert "no host was given" in result.exception.__str__()


@patch("noora.shell.Shell.Shell.execute")
def test_deploy_invalid_environment_fail(command: MagicMock):
    """
    This test passes when a PluginException is raised, with the message
    environment 'unknown_environment' is not valid for this project.
    """

    # set the SQL output, an empty string means the SQL statement is successfully executed
    command.return_value = ""

    # read the properties from myproject.json, normally handled by mynoora_cli
    props = Properties()

    runner = CliRunner()
    result = runner.invoke(deploy, obj=props, args=["--environment", "unknown_environment"])

    print(f"exception={result.exception}")
    assert result.exit_code == 1
    assert "environment 'unknown_environment' is not valid for this project" in result.exception.__str__()
