.. _validation:

Validation
==========

xlea supports per-column value validation before type conversion.
A validator is a plain callable that returns ``True`` if the value is
acceptable and ``False`` otherwise.


Attaching a validator
---------------------

Pass any ``Callable[[Any], bool]`` to the ``validator`` argument of
:func:`~xlea.Column`:

.. code-block:: python

   from xlea import Schema, Column

   class Employee(Schema):
       id: int  = Column("ID", validator=lambda v: str(v).isnumeric())
       age: int = Column("Age", validator=lambda v: 0 < int(v) < 120)

The validator receives the **raw cell value** (before type conversion).
This means you should handle the value as a string or whatever the provider
returns — not as the annotated type.

Raise vs skip
-------------

By default, a failed validator raises :exc:`~xlea.exc.InvalidRowError`.
Set ``skip_invalid_row=True`` to silently drop the row instead:

.. code-block:: python

   class Sale(Schema):
       amount: float = Column(
           "Amount",
           validator=lambda v: str(v).replace(".", "", 1).lstrip("-").isnumeric(),
           skip_invalid_row=True,
       )

   # rows where "Amount" is "N/A", "-", or "" are silently omitted
   for sale in xlea.autoread("sales.xlsx", schema=Sale):
       print(sale.amount)

Multiple validators
-------------------

xlea supports only one validator per column. Combine conditions with ``and``:

.. code-block:: python

   is_valid_age = lambda v: str(v).isnumeric() and 0 < int(v) < 150

   class Person(Schema):
       age: int = Column("Age", validator=is_valid_age, skip_invalid_row=True)

Validator return type
---------------------

The validator **must** return a ``bool``. Returning any other type (e.g. a
truthy integer or a string) raises
:exc:`~xlea.exc.IncompatibleReturnValueTypeError`:

.. code-block:: python

   # ✗ Wrong — str() is truthy but not bool
   Column("Age", validator=str)

   # ✓ Correct
   Column("Age", validator=lambda v: bool(str(v)))

.. warning::

   ``bool`` itself is a valid validator because ``bool(value)`` returns
   ``True`` or ``False``. It will mark empty strings, ``0``, and ``None``
   as invalid.

Real-world example
------------------

A schema that reads a sales report and skips rows with missing or
non-numeric amounts:

.. code-block:: python

   import xlea
   from xlea import Schema, Column

   def is_numeric(v) -> bool:
       try:
           float(str(v))
           return True
       except ValueError:
           return False

   class SalesRow(Schema):
       date: str    = Column("Date")
       product: str = Column("Product")
       revenue: float = Column(
           "Revenue",
           validator=is_numeric,
           skip_invalid_row=True,
       )

   total = sum(
       row.revenue
       for row in xlea.autoread("sales_report.xlsx", schema=SalesRow)
   )
   print(f"Total revenue: {total:.2f}")
