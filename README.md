# Artemis Client

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![GitHub issues](https://img.shields.io/github/issues/kit-sdq/artemis_client.svg?style=square)](https://github.com/kit-sdq/artemis_client/issues)
[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg?style=square)](https://github.com/kit-sdq/artemis_client/blob/main/LICENSE.md)

## Installation
```bash
pip install git+https://github.com/kit-sdq/artemis_client@main
```

## Configuration
The client can be configured either by configuration file or by environment variables.

- Provide a file 'config.ini' in the working directory
- Provide a file 'config.ini' in a custom directory and set ARTEMIS_CLIENT_CONFIG environment variable accordingly
- Provide all configuration options as environment variables (SECTION_KEY)
- Supply username and password using the `Session` constructor

Values found in environment variables are preferred over configuration files. That can be used to provide credentials in a testing environment, for example.


## Setting up a development environment

This project uses [poetry](https://python-poetry.org/):
```bash
poetry install
```


### Testing

```bash
poetry run tox  # thats all
```

### Folder layout
This project uses the "Tests outside application code" layout presented [here](https://docs.pytest.org/en/6.2.x/goodpractices.html#test-discovery) (sources in src folder).

### Build the docs
You can build the documentation using sphinx:

```bash
poetry run tox -e docs
```

The docs can then be found in `.tox/docs_out`
