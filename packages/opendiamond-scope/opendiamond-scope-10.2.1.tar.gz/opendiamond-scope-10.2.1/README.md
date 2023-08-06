# OpenDiamond-scope

Library and tools for manipulating OpenDiamond search scopes.


# To install the latest release from PyPI

    pipx install opendiamond-scope          # or
    pip install --user opendiamond-scope


# Building from source

For development, a consistent development environment is managed with poetry.
If you are developing locally it is recommended to set up pre-commit git hooks.

    poetry install
    poetry run pre-commit install   # optional

The code can then be run from the managed environment.

    poetry run opendiamond-scope -h

Running of tests and release tagging is done with nox, which should already be
installed in the development environment at this point.

    # run tests against different installed python interpreters
    poetry run nox

    # release version tagging (and publishing) are handled by a nox script
    poetry run nox -s release -- [major/minor/patch]
