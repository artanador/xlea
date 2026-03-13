.. _multi_row_headers:

Multi-row Headers
=================

Some spreadsheets use two or more header rows — typically a category row
followed by a sub-header row. xlea handles this with the ``@config``
decorator.

.. contents:: On this page
   :local:

Example spreadsheet layout
---------------------------

Consider a file where the header spans two rows:

.. code-block:: text

   Row 1 (category):  │ Profile       │ Profile       │ Contact │
   Row 2 (sub-header):│ Last Name     │ First Name    │ Email   │
   Row 3 (data):      │ Smith         │ Alice         │ a@x.com │
   Row 4 (data):      │ Jones         │ Bob           │ b@x.com │

xlea flattens these into ``"Profile;Last Name"``, ``"Profile;First Name"``,
``"Contact;Email"`` (using ``;`` as the default delimiter).

Configuration
-------------

Use ``@config(header_rows=2)`` on your schema class:

.. code-block:: python

   from xlea import Schema, Column, config

   @config(header_rows=2)
   class Person(Schema):
       last_name: str  = Column("Profile;Last Name")
       first_name: str = Column("Profile;First Name")
       email: str      = Column("Contact;Email")

The first segment is carried forward when a category cell is empty (merged
cells). So the spreadsheet above is equivalent to:

.. code-block:: text

   Profile;Last Name  │ Profile;First Name │ Contact;Email

Custom delimiter
----------------

The default delimiter between header levels is ``;``. Override it with
``delimiter``:

.. code-block:: python

   @config(header_rows=2, delimiter=" / ")
   class Report(Schema):
       revenue: float = Column("Finance / Revenue (USD)")

You can combine a custom delimiter with ``ignore_case`` on individual columns:

.. code-block:: python

   @config(header_rows=2, delimiter="|")
   class Inventory(Schema):
       sku: str   = Column("Product|SKU", ignore_case=True)
       qty: int   = Column("Stock|Quantity")

How carry-forward works
-----------------------

When a category cell is empty (or contains only whitespace / ``None``), xlea
reuses the last seen non-empty value for that column position. This mirrors
how merged cells look when exported from Excel.

Given:

.. code-block:: text

   │ Sales  │        │ Finance │        │
   │ Q1     │ Q2     │ Q1      │ Q2     │

xlea produces: ``["Sales;Q1", "Sales;Q2", "Finance;Q1", "Finance;Q2"]``

.. code-block:: python

   @config(header_rows=2)
   class Quarterly(Schema):
       sales_q1:   float = Column("Sales;Q1")
       sales_q2:   float = Column("Sales;Q2")
       finance_q1: float = Column("Finance;Q1")
       finance_q2: float = Column("Finance;Q2")
