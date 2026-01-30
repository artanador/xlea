# XLEA

`xlea` is a python library that makes it easy to convert Excel tables into ORM-like objects.

The library focised on **schema-driven** parsing of tabular data, where column resolution, validation and type conversion are handled explicitly and predictably.

> ⚠️ XLEAA is a work in progress. The public API is stabilizing, and core concepts are already in place.

## Features

- Declarative schema definition
Describe tabular data using Python classes with type annotations and column descriptors.

- Automatic column resolution
Columns are matched by name, regular expression, or custom predicate — no hard-coded indexes.

- Type-driven value conversion
Cell values are automatically cast using schema type annotations with explicit error reporting.

- Header-aware parsing
Support for multi-row headers and complex header layouts via schema configuration.

- Pluggable provider architecture
File formats are handled by interchangeable providers, selected automatically by file extension.

- Excel formats out of the box
Native support for .xlsx, .xls, and .xlsb via dedicated providers.

- Row-level validation
Custom validators can be attached to columns to enforce domain-specific constraints.

- Graceful handling of invalid data
Optionally skip rows with invalid values instead of failing the entire read.

## Example

### Defining a Schema

```python
from typing import Optional

from xlea import Schema, Column


age_name = lambda name: name.startswith("Age")
age_validator = lambda val: val.isnumeric()

@config(header_rows=2)
class Person(Schema):
    id: str = Column("ID")
    fullname: str = Column("Profile;Last Name, First Name", ignore_case=True)
    age: int = Column(age_name, validator=age_validator, skip_invalid_row=True)
    city: Optional[str] = Column("City", required=False, default="Voronezh")
```

### Reading an Excel file

```python
import xlea
from xlea.providers.openpyxl import OpenPyXlProvider

from schemas import Person


def main():
    persons = xlea.read(OpenPyXlProvider("test_data.xlsx"), schema=Person)
    # or with automatic provider selection
    persons = xlea.autoread("test_data.xlsx", schema=Person)

    for p in persons:
        print(p.id, p.fullname, p.age)


if __name__ == "__main__":
    main()
```
