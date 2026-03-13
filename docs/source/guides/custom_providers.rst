.. _custom_providers:

Custom Providers
================

A **provider** is any object with a ``rows()`` method that returns an
iterable of rows (each row being an iterable of cell values). This design
lets you feed xlea from CSV files, databases, in-memory lists, or any
other tabular source.


The provider protocol
---------------------

.. code-block:: python

   class MyProvider:
       def rows(self) -> Iterable[Iterable]:
           ...

That's the entire contract. No base class required.

In-memory provider (testing)
-----------------------------

Useful for unit tests — no file I/O needed:

.. code-block:: python

   from xlea import Schema, Column, read

   class Order(Schema):
       id: int    = Column("ID")
       product: str = Column("Product")

   class ListProvider:
       def __init__(self, rows):
           self._rows = rows

       def rows(self):
           return iter(self._rows)

   data = [
       ("ID", "Product"),
       (1, "Widget"),
       (2, "Gadget"),
   ]

   for order in read(ListProvider(data), schema=Order):
       print(order.id, order.product)

CSV provider
------------

.. code-block:: python

   import csv
   from xlea import Schema, Column, read

   class CSVProvider:
       def __init__(self, path, encoding="utf-8"):
           self._path = path
           self._encoding = encoding

       def rows(self):
           with open(self._path, newline="", encoding=self._encoding) as f:
               yield from csv.reader(f)

   class Person(Schema):
       name: str = Column("Name")
       age: int  = Column("Age")

   for person in read(CSVProvider("people.csv"), schema=Person):
       print(person.name)

Database provider (SQLite example)
------------------------------------

.. code-block:: python

   import sqlite3
   from xlea import Schema, Column, read

   class SQLiteProvider:
       def __init__(self, db_path, query):
           self._db_path = db_path
           self._query = query

       def rows(self):
           conn = sqlite3.connect(self._db_path)
           cursor = conn.execute(self._query)
           # yield column names as header row first
           yield [desc[0] for desc in cursor.description]
           yield from cursor
           conn.close()

   class Product(Schema):
       id: int    = Column("id")
       name: str  = Column("name")
       price: float = Column("price")

   provider = SQLiteProvider("shop.db", "SELECT id, name, price FROM products")
   for product in read(provider, schema=Product):
       print(product.name, product.price)

Registering a provider for autoread
-------------------------------------

If you want :func:`~xlea.autoread` to pick your provider automatically by
file extension, use :func:`~xlea.register_provider`:

.. code-block:: python

   import xlea
   from xlea import register_provider

   class CSVProvider:
       def __init__(self, path, sheet=None):  # sheet ignored for CSV
           self._path = path

       def rows(self):
           import csv
           with open(self._path, newline="") as f:
               yield from csv.reader(f)

   register_provider(".csv", CSVProvider)

   # Now autoread works with .csv files:
   for row in xlea.autoread("data.csv", schema=MySchema):
       print(row)

.. note::

   The provider constructor must accept ``(path, sheet=None)`` to be
   compatible with :func:`~xlea.autoread`.
