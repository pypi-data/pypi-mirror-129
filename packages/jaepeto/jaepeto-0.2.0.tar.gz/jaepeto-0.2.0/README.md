# Automated Technical Docs

Code to automatically generate technical documentation
from a codebase. The code is compiled into a VSCode Extension
in Python via [`vscode-ext`][vscode-ext].

## Get started

### Requirements

- Developed with `python 3.9`
- `pip install -r requirements.txt`
- `pip install -r requirements-dev.txt`
- `pip install -e .`

Packages are required to be installed locally
at this time
in order to build the VSCode extension
([vcsode-ext] doesn't currently recognise virtual environments).

### Compile Extensions

Run `python extension.py` to build the extension.
On this repo in VSCode,
run `F5` to launch a dev editor,
in which the custom extensions will be present.

## Style Guide

- Use `black` to format code
- Other than `black` niches, adhere to PEP
- Use `isort` to sort imports
- Use numpy-style docstrings
- Use type hints and verify with `mypy`

## Testing

Testing performed with `pytest`.
Run `python -m pytest`
to run unit tests.

[vscode-ext]: https://github.com/CodeWithSwastik/vscode-ext/
