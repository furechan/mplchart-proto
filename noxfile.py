import os
import nox
import tempfile

VERSIONS = ["3.9", "3.10", "3.11", "3.12"]

ENVDIR = os.path.join(tempfile.gettempdir(), "nox")

nox.options.envdir = ENVDIR
nox.options.default_venv_backend = "uv"


@nox.session(python=VERSIONS)
def tests(session: nox.Session):
    session.install(".", "pytest")
    session.run("pytest")


@nox.session()
def lint(session: nox.Session):
    session.install("ruff")
    session.run("ruff", "check")
