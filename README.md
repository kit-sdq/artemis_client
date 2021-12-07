# Artemis Client

## Configuration
The client can be configured either by configuration file or by environment variables.

- Provide a file 'config.ini' in the working directory
- Provide a file 'config.ini' in a custom directory and set ARTEMIS_CLIENT_CONFIG environment variable accordingly
- Provide all configuration options as environment variables (SECTION_KEY)

Values found in environment variables are preferred over configuration files. That can be used to provide credentials in a testing environment, for example.


## Setting up a development environment
```bash
# OPTIONAL: Create a venv
python -m venv env
source env/bin/activate # Unix
# .\env\Scripts\activate  # Windows


# Install dev dependencies
pip install --upgrade --force-reinstall -r requirements.txt
```


### Testing

```bash
tox  # thats all
```

### Folder layout
This project uses the "Tests outside application code" layout presented [here](https://docs.pytest.org/en/6.2.x/goodpractices.html#test-discovery) (sources in src folder). 