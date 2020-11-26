
import tempfile
from pathlib import Path
import os
import pytest
import subprocess
from quetz import cli as qcli


def quetz_cmd(cmd, *args):
    """Run the tox suite of the newly created plugin."""
    try:
        subprocess.check_call([
            "quetz",
            cmd,
        ] + list(args))
    except subprocess.CalledProcessError as e:
        pytest.fail(e)


def test_run_tests(plugin):
    """Run the tox suite of the newly created plugin."""
    try:
        subprocess.check_call([
            "pytest",
            plugin,
        ])
    except subprocess.CalledProcessError as e:
        pytest.fail(e)


@pytest.fixture
def quetz_deployment():
    deploy_dir = Path(tempfile.mkdtemp()) / 'deployment'

    quetz_cmd("create", deploy_dir, '--create-conf')

    yield deploy_dir


def test_initialize_migrations(plugin, quetz_deployment):
    deploy_dir = quetz_deployment

    quetz_cmd("make-migrations", deploy_dir, '--plugin', "quetz-foo_bar", "--message", "initial foo_bar revision", "--initialize")
    plugin_dir = Path(plugin)
    version_location = plugin_dir / "quetz_foo_bar" / "migrations" / "versions"
    migration_scripts = list(version_location.glob("*initial_foo_bar_revision.py"))
    assert migration_scripts

@pytest.fixture
def plugin(cookies):
    """Create a new plugin via cookiecutter and install it."""
    result = cookies.bake(extra_context={'plugin_name': 'foo_bar'})

    assert result.exit_code == 0
    assert result.exception is None
    assert result.project.basename == 'quetz_foo_bar'
    assert result.project.isdir()
    assert result.project.join('quetz_foo_bar/main.py').isfile()
    assert result.project.join('tests', 'test_main.py').isfile()

    try:
        subprocess.check_call(["python", "-m", "pip", "install", "-e", result.project])
        yield str(result.project)
    except subprocess.CalledProcessError as e:
        pytest.fail(e)
    subprocess.check_call(["pip", "uninstall", "foo_bar", "-y"])
