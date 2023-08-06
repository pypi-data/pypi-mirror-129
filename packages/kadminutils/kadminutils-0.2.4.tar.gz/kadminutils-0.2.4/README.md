# kadminutils

kadmin.local wrapper

## Install

```
pip install kadminutils
```

## Requirements

The library wraps the command `kadmin.local` and `kinit`, so you must put these two command in PATH.

## Functions

- list_principals
- delete_principal
- change_password
- get_principal
- rename_principal
- ktadd
- check_password


## Example

```
import kadminutils
import uuid
import os

realm = os.environ.get("KRB5REALM", "EXAMPLE.COM")

principal = str(uuid.uuid4()) + "@" + realm
principal2 = str(uuid.uuid4()) + "@" + realm
password = str(uuid.uuid4())

r1 = kadminutils.add_principal(principal)
print(r1)

r2 = kadminutils.change_password(principal)
print(r2)

r3 = kadminutils.change_password(principal, password)
print(r3)

r4 = kadminutils.get_principal(principal)
print(r4)

r5 = kadminutils.rename_principal(principal, principal2)
print(r5)

r6 = kadminutils.check_password(principal2, password)
print(r6)

r7 = kadminutils.ktadd("/tmp/a.keytab", [principal2])
print(r7)

r8 = kadminutils.delete_principal(principal2)
print(r8)

r9 = kadminutils.list_principals()
print(r9)

os.unlink("/tmp/a.keytab")

```

## Releases

### v0.2.4 2021/12/03

- First release.
