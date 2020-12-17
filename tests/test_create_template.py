
import tempfile
from pathlib import Path
import os
import pytest
import subprocess
from quetz import cli as qcli


def shell_cmd(*args):
    try:
        output = subprocess.check_output(
                list(args), stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError as e:
        pytest.fail(e.output.decode())
    return output.decode()


def quetz_cmd(cmd, *args):
    """Run the tox suite of the newly created plugin."""
    return shell_cmd("quetz", cmd, *args)


def test_run_tests(plugin_dir, install_plugin):
    """Run the tox suite of the newly created plugin."""
    shell_cmd("pytest", plugin_dir)

@pytest.fixture
def deploy_dir():

    deploy_dir = Path(tempfile.mkdtemp()) / 'deployment'
    return deploy_dir

@pytest.fixture
def quetz_deployment(deploy_dir):

    quetz_cmd("create", deploy_dir, '--create-conf')

    yield deploy_dir


@pytest.mark.parametrize("use_quetz", [False])
def test_initialize_migrations(install_plugin, quetz_deployment, deploy_dir, capsys, plugin_dir):

    quetz_cmd("make-migrations", deploy_dir, '--plugin', "quetz-foo_bar", "--message", "initial foo_bar revision", "--initialize")
    plugin_dir = Path(plugin_dir)
    version_location = plugin_dir / "quetz_foo_bar" / "migrations" / "versions"
    migration_scripts = list(version_location.glob("*initial_foo_bar_revision.py"))
    assert migration_scripts

    output = quetz_cmd("init-db", deploy_dir)

    assert "initial foo_bar revision" in output

@pytest.fixture
def use_quetz(quetz_deployment):
    return True

@pytest.fixture
def plugin_dir(cookies):
    """Create a new plugin via cookiecutter and install it."""
    result = cookies.bake(extra_context={'plugin_name': 'foo_bar'})

    assert result.exit_code == 0
    assert result.exception is None
    assert result.project.basename == 'quetz_foo_bar'
    assert result.project.isdir()
    assert result.project.join('quetz_foo_bar/main.py').isfile()
    assert result.project.join('tests', 'test_main.py').isfile()

    return result.project

@pytest.fixture
def install_plugin(plugin_dir, use_quetz):
    if use_quetz:
        quetz_cmd("plugin", "install", plugin_dir)
    else:
        shell_cmd("pip", "install", "-e", plugin_dir)

    yield plugin_dir
    shell_cmd("pip", "uninstall", "quetz-foo_bar", "-y")
