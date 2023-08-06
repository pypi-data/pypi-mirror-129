[![PyPI version](https://badge.fury.io/py/pycert.svg)](https://badge.fury.io/py/pycert)

# Certificate

The cross-platform tool to get certificate info (including self-signed).

## Installation

For most users, the recommended method to install is via pip:

```cmd
pip install pycert
```

## Import

```python
from pycert import CertClient
```

---

## Usage

#### Command from usual user:

```python
from pycert import CertClient

client = CertClient(host="172.16.0.124")
print(client.get_all_info())

```

##### 0.0.1 (30.11.2021)

- initial commit