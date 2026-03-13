.. _concepts:

Core Concepts
=============

This page explains how xlea works internally. Understanding these concepts
will help you use the library predictably and debug edge cases.

.. contents:: On this page
   :local:
   :depth: 2

The Schema
----------

A **schema** is a Python class that inherits from :class:`~xlea.Schema` and
declares :func:`~xlea.Column` descriptors as class attributes.

.. code-block:: python

   from xlea import Schema, Column

   class Order(Schema):
       order_id: int   = Column("Order ID")
       product: str    = Column("Product Name")
       quantity: int   = Column("Qty")

The schema serves three purposes simultaneously:

1. **Column declaration** — tells xlea what to look for in the header row
2. **Type conversion** — the type annotation drives automatic casting
3. **Row interface** — each data row is returned as an instance of the schema

When xlea iterates a file, it never modifies your schema class. Instead, it
creates a lightweight *bound* version that holds the resolved column indices
for that specific file.

Header resolution
-----------------

Before iterating data rows, xlea scans the file for a **header row** — a row
where every required column can be matched. This scan is automatic and
position-independent: the header can be on row 1, row 5, or anywhere else.

The algorithm:

1. Read rows one by one from the provider
2. For each row, check whether all required columns match any cell value
3. The first row that satisfies all required columns becomes the header
4. All rows after the header (offset by ``header_rows``) are data rows

.. note::

   Header detection is **eager** — it happens at the ``read()`` call site,
   not lazily during iteration. If no matching header is found,
   :exc:`~xlea.exc.HeaderNotFound` (or :exc:`~xlea.exc.MissingRequiredColumns`
   with a helpful message) is raised immediately.

Column binding
--------------

Once a header row is found, xlea **binds** each ``Column`` descriptor to its
integer index in that row. This index is used for every subsequent data row
— there are no per-row lookups.

Optional columns (``required=False``) that are not found in the header are
simply left unbound and return their ``default`` value when accessed.

Type conversion
---------------

If a schema attribute has a type annotation, xlea calls that type as a
constructor on the raw cell value:

.. code-block:: python

   class Report(Schema):
       year: int   = Column("Year")    # int("2026") → 2026
       rate: float = Column("Rate")    # float("0.15") → 0.15
       label: str  = Column("Label")  # str(42) → "42"

If conversion fails (e.g. ``int("N/A")``), a :exc:`TypeError` is raised with
a descriptive message including the row index and expected type.

Row objects
-----------

Each row yielded by :func:`~xlea.read` / :func:`~xlea.autoread` is an
instance of a dynamically created class that inherits from both your schema
and ``RowObject``. This means:

- ``person.name`` — attribute access, type-converted
- ``person["Full Name"]`` — column-name subscript (raw header value)
- ``person[0]`` — positional subscript (0 = first bound column)
- ``person.asdict()`` — ``{"name": "Alice", ...}`` with all declared columns
- ``person.row_index`` — 0-based index within the data section
- ``"Full Name" in person`` — membership test by column name

.. code-block:: python

   for row in xlea.autoread("data.xlsx", schema=Order):
       d = row.asdict()
       print(d)  # {"order_id": 42, "product": "Widget", "quantity": 3}

Invalid rows
------------

Two strategies are available for rows that fail validation:

**Raise** (default): if a row contains an invalid value, an
:exc:`~xlea.exc.InvalidRowError` is raised immediately.

**Skip**: set ``skip_invalid_row=True`` on the column whose validator may
fail. Rows that fail that validator are silently omitted from the iterator.

.. code-block:: python

   class Sale(Schema):
       amount: float = Column(
           "Amount",
           validator=lambda v: str(v).replace(".", "").isnumeric(),
           skip_invalid_row=True,  # skip rows like "N/A" or "-"
       )

Empty rows
----------

Providers sometimes emit empty tuples ``()`` for blank rows in the spreadsheet
(common with openpyxl and xlrd). xlea normalises these automatically by
padding them to the required length, so they pass through the validation
pipeline — and are skipped or error as expected, never crash with an
``IndexError``.
