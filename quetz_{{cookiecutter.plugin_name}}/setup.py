from setuptools import setup

setup(
    name="quetz-{{cookiecutter.plugin_name}}",
    install_requires="quetz",
    entry_points={"quetz": ["quetz-{{cookiecutter.plugin_name}} = quetz_{{cookiecutter.plugin_name}}.main"]},
    packages=["quetz_{{cookiecutter.plugin_name}}"],
)
