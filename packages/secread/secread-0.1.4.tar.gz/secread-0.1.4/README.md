## Thycotic Secret Server Reader

This Python module allows to retrive secrets from Thycotic Secret Server.
It utilizes the REST API

see:
<https://docs.thycotic.com/ss/10.8.0/api-scripting/rest-api-reference-download>

### License

MIT

### Installation

Installation with `PyPi`:

```bash
pip install secread
```

Installation with `poetry`:

```bash
poetry add secread
```

### Configuration

To configure the module use following environment variables. It is also possible
to provide the file '.env' with the settings

```bash
# copy the template as environment file
cp .env.example .env

# Edit configuration file
vi .env
```

```python
#############################################################################
# Settings for Thycotic Secret Server Reader

SECRET_SERVER_SITE='https://pw.example.com/SecretServer'
SECRET_SERVER_AUTH_API='/oauth2/token'
SECRET_SERVER_USERNAME='apiuser'
SECRET_SERVER_PASSWORD='my_password_for_apiuser'

# Values for SECRET_SERVER_SSL_VERIFY
# - True    server certificate will be verified (Default)
# - False   server certificate will be ignored; warning
# - Path    path to trusted cerificate bundle e.g. '/etc/ssl/certs/ca-bundle.trust.crt'
SECRET_SERVER_SSL_VERIFY='/etc/ssl/certs/ca-bundle.trust.crt'

# Default field-items to extract from result.
SECRET_SERVER_DEFAULT_SLUGS='["id", "url", "username", "password"]'

# SECRET_SERVER_IS_DUMMY (Default: False)
# - False: Secert-Server-API is active
# - True: The API will not be used. SECRET_SERVER_TEST_DUMMY_RESULT will be returned
# SECRET_SERVER_IS_DUMMY=False

SECRET_SERVER_TEST_DUMMY_RESULT='{"id": "12345", username": "testuser", "password": "testpassword", "url": "https://localhost/SecretServer"}'

# 'name' of the secret that is used for testing on live server
# TEST_SECRET_NAME='GitLab Token netsearch-ro'
```

### Development

The installation instruction for `poetry` is here: <https://python-poetry.org/docs/#installation>

```bash
git clone https://github.com/jifox/secret-server-reader.git
cd secret-server-reader

# Set python environment to use for development
# poetry env use python3.8

# Install the module
poetry install

# Execute tests (be sure to configure the system before)
poetry run pytest -v
```

#### Update pypi

Before updating pypi, the version number must be incremented in following files:

- pyproject.toml
- secread/__init__.py
- secread/tests/test_secread.py

```bash
poetry build
poetry publish
```

### Examples

```python
"""Tests for module secread"""
import os
import pytest
from secread import __version__, SecretServer


def test_version():
    assert __version__ == "0.1.1"


@pytest.fixture
def sec_server():
    return SecretServer()


def test_default_slugs_is_a_list(sec_server: SecretServer):
    slugs = sec_server.SECRET_SERVER_DEFAULT_SLUGS
    assert isinstance(slugs, list)


def test_secretserver(sec_server: SecretServer):
    token = sec_server.getAuthToken()
    assert len(token) > 0, "Token could not be read"


def test_get_secret_response_by_name(sec_server: SecretServer):
    secname = os.getenv("TEST_SECRET_NAME", "GitLab Token netsearch-ro")
    res = sec_server.searchSecretResponse(secname)
    fields = sec_server.getFieldItemWithSlug(res)
    assert "username" in fields.keys(), "Missing username"
    assert "password" in fields.keys(), "Missing password"


def test_get_secret_by_name(sec_server: SecretServer):
    secname = os.getenv("TEST_SECRET_NAME", "GitLab Token netsearch-ro")
    res = sec_server.searchSecret(secname)
    assert "username" in res.keys(), "Missing username"
    assert "password" in res.keys(), "Missing password"
```
