.. _api-schema:

Schema & config
===============

.. autoclass:: xlea.Schema
   :members:
   :show-inheritance:

----

.. autofunction:: xlea.config

----

Usage example
-------------

.. code-block:: python

   from xlea import Schema, Column, config

   # Simple schema — single header row (default)
   class Person(Schema):
       id: int   = Column("ID")
       name: str = Column("Name")

   # Schema with two header rows and a custom delimiter
   @config(header_rows=2, delimiter=" > ")
   class Report(Schema):
       revenue: float = Column("Finance > Revenue")
       units: int     = Column("Sales > Units Sold")
