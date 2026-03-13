.. _quickstart:

Quickstart
==========

This page walks you through the essential xlea workflow in five minutes.

Step 1 — Define a schema
-------------------------

A schema is a plain Python class that describes the columns you care about.
Each attribute is a :func:`~xlea.Column` descriptor paired with a type annotation.

.. code-block:: python

   from xlea import Schema, Column

   class Person(Schema):
       id: int      = Column("ID")
       name: str    = Column("Full Name", ignore_case=True)
       age: int     = Column("Age")
       city: str    = Column("City", required=False, default="Unknown")

xlea will find columns by their header name, convert values using the
annotated type, and expose them as attributes on each row object.

Step 2 — Read a file
---------------------

Use :func:`~xlea.autoread` to let xlea pick the right provider automatically
based on file extension:

.. code-block:: python

   import xlea

   for person in xlea.autoread("employees.xlsx", schema=Person):
       print(person.id, person.name, person.age, person.city)

Or pick a provider explicitly if you need more control:

.. code-block:: python

   from xlea import read
   from xlea.providers.openpyxl import OpenPyXlProvider

   provider = OpenPyXlProvider("employees.xlsx", sheet="Q1")
   for person in xlea.read(provider, schema=Person):
       print(person.name)

Step 3 — Work with row objects
-------------------------------

Each row is a full Python object. You can access values as attributes,
convert to a dict, or use subscript access:

.. code-block:: python

   for person in xlea.autoread("employees.xlsx", schema=Person):
       # Attribute access (type-converted)
       print(person.age + 1)

       # Dict conversion
       data = person.asdict()
       # {"id": 1, "name": "Alice", "age": 30, "city": "Berlin"}

       # Column name subscript
       print(person["Full Name"])

       # Zero-based positional subscript
       print(person[0])  # first declared column

       # Row index in the file (0 = first data row)
       print(person.row_index)

       # Membership test
       if "Full Name" in person:
           print("has name")

What's next?
------------

- :doc:`concepts` — understand how column resolution, header detection, and
  type conversion work under the hood
- :doc:`column_matching` — string, regex, callable, and case-insensitive patterns
- :doc:`validation` — per-column validators and skipping invalid rows
- :doc:`multi_row_headers` — ``@config(header_rows=2)`` for merged/hierarchical headers
- :doc:`custom_providers` — reading CSV, databases, or any tabular source
