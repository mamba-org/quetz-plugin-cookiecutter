from setuptools import setup

setup(
    name="quetz-{{cookiecutter.plugin_name}}",
    install_requires="quetz",
    entry_points={
        "quetz": ["quetz-{{cookiecutter.plugin_name}} = quetz_{{cookiecutter.plugin_name}}.main"],
        "quetz.models": ["quetz-{{cookiecutter.plugin_name}} = quetz_{{cookiecutter.plugin_name}}.db_models"],
        "quetz.migrations": ["quetz-{{cookiecutter.plugin_name}} = quetz_{{cookiecutter.plugin_name}}.migrations"]
        },
    packages=[
        "quetz_{{cookiecutter.plugin_name}}",
        "quetz_{{cookiecutter.plugin_name}}.migrations",
        "quetz_{{cookiecutter.plugin_name}}.migrations.versions",
        ],
)
