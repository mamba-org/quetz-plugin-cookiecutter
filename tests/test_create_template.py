
import os
import pytest
import subprocess


def run_tests(plugin):
    """Run the tox suite of the newly created plugin."""
    try:
        subprocess.check_call([
            "pytest",
            plugin,
        ])
    except subprocess.CalledProcessError as e:
        pytest.fail(e)


def test_run_cookiecutter_and_plugin_tests(cookies):
    """Create a new plugin via cookiecutter and run its tests."""
    result = cookies.bake(extra_context={'plugin_name': 'foo_bar'})

    assert result.exit_code == 0
    assert result.exception is None
    assert result.project.basename == 'quetz_foo_bar'
    assert result.project.isdir()
    assert result.project.join('quetz_foo_bar/main.py').isfile()
    assert result.project.join('tests', 'test_main.py').isfile()

    try:
        subprocess.check_call(["python", "setup.py", "install"], cwd=result.project)
    except subprocess.CalledProcessError as e:
        pytest.fail(e)

    run_tests(str(result.project))
