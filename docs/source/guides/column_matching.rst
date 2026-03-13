.. _column_matching:

Column Matching
===============

xlea supports four strategies for matching a column descriptor to a header
cell. All strategies are set via the ``pattern`` argument of
:func:`~xlea.Column`.

.. contents:: On this page
   :local:

Exact string match
------------------

The simplest case — the pattern must equal the header value exactly:

.. code-block:: python

   class Report(Schema):
       total: float = Column("Total (USD)")

Case-insensitive match
----------------------

Pass ``ignore_case=True`` to match regardless of casing:

.. code-block:: python

   class Report(Schema):
       name: str = Column("client name", ignore_case=True)
       # matches: "Client Name", "CLIENT NAME", "client name", …

.. note::

   ``ignore_case`` has no effect when the ``pattern`` is a compiled
   :class:`re.Pattern`. Apply flags directly to the pattern instead:
   ``re.compile(r"name", re.IGNORECASE)``.

Regular expression
------------------

Pass a compiled :class:`re.Pattern` **or** set ``regexp=True`` on a string:

.. code-block:: python

   import re
   from xlea import Schema, Column

   class Sales(Schema):
       # Compiled pattern — re.IGNORECASE applied directly
       revenue: float = Column(re.compile(r"revenue", re.IGNORECASE))

       # String + regexp=True — compiled without flags
       units: int = Column(r"^Units\s*\(.*\)$", regexp=True)

The pattern is matched with :func:`re.search`, so it can match anywhere
in the header value unless anchored with ``^`` / ``$``.

Callable predicate
------------------

For full control, pass any callable that takes a ``str`` and returns ``bool``:

.. code-block:: python

   class Forecast(Schema):
       q1: float = Column(lambda h: h.startswith("Q1"))
       q2: float = Column(lambda h: h.startswith("Q2"))

   # or with a named function for clarity:
   def is_revenue_col(header: str) -> bool:
       return "revenue" in header.lower() and "net" not in header.lower()

   class Report(Schema):
       revenue: float = Column(is_revenue_col)

Combining strategies
--------------------

Different columns in the same schema can use different strategies:

.. code-block:: python

   import re
   from xlea import Schema, Column

   class Invoice(Schema):
       id: int      = Column("Invoice ID")                          # exact
       client: str  = Column("client", ignore_case=True)           # case-insensitive
       amount: float = Column(re.compile(r"amount", re.I))         # regex
       note: str    = Column(lambda h: "note" in h.lower(),        # callable
                             required=False, default="")
