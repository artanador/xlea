.. xlea documentation master file

####
xlea
####

*Schema-driven Excel parsing for Python.*

``xlea`` converts Excel rows into typed Python objects — with automatic column
resolution, value validation, and graceful error handling.
No hard-coded indexes. No brittle column slicing. Just a clean schema class
and a one-liner to iterate your data.

.. code-block:: python

   from xlea import Schema, Column
   import xlea

   class Invoice(Schema):
       id: int = Column("Invoice ID")
       client: str = Column("Client Name", ignore_case=True)
       total: float = Column("Total (USD)")

   for row in xlea.autoread("invoices.xlsx", schema=Invoice):
       print(row.id, row.client, row.total)

----

.. rubric:: Navigation

.. toctree::
   :maxdepth: 1
   :caption: Getting Started

   guides/installation
   guides/quickstart
   guides/concepts

.. toctree::
   :maxdepth: 1
   :caption: How-to Guides

   guides/column_matching
   guides/validation
   guides/multi_row_headers
   guides/custom_providers

.. toctree::
   :maxdepth: 1
   :caption: API Reference

   api/reader
   api/schema
   api/column
   api/providers
   api/exceptions

.. toctree::
   :maxdepth: 1
   :caption: Project

   changelog
