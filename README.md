# XLEA

`xlea` - is a python library that makes it easy to convert Excel tables into ORM-like objects.

This library is a work in progress. The current implementation provides basic functionality for defining schemas and reading Excel files intro python objects.

## Features

- Define Excel table schemas as python classes.
- Automatically map Excel columns to class attributes.
- Support optional and required fields.
- Easily extendable with different providers based on the `ProviderProto`.

## Example

### Defining a Schema

```python
from xlea import Schema, Column


class Person(Schema):
    id = Column("ID")
    fullname = Column("ФИО", ignore_case=True)
    age = Column("Возраст")
    city = Column("город", required=False)
```

### Reading an Excel file

```python
import xlea
from xlea.providers.openpyxl import OpenPyXlProvider

from schemas import Person


def main():
    persons = xlea.read(OpenPyXlProvider("test_data.xlsx"), schema=Person)

    for p in persons:
        print(p.id, p.fullname, p.age)


if __name__ == "__main__":
    main()
```
