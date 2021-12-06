# Artemis Client


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