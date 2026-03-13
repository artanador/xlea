.. _api-column:

Column
======

.. autofunction:: xlea.Column

----

Matching strategies at a glance
---------------------------------

.. list-table::
   :header-rows: 1
   :widths: 30 70

   * - Pattern type
     - Behaviour
   * - ``str``
     - Exact match (or case-insensitive with ``ignore_case=True``)
   * - ``str`` + ``regexp=True``
     - Compiled to :class:`re.Pattern`, matched with :func:`re.search`
   * - :class:`re.Pattern`
     - Matched with :func:`re.search`; ``ignore_case`` is ignored
   * - ``Callable[[str], bool]``
     - Called with each header cell; first ``True`` wins

Examples
--------

.. code-block:: python

   import re
   from xlea import Schema, Column

   class Invoice(Schema):
       # Exact match
       invoice_id: int = Column("Invoice ID")

       # Case-insensitive
       client: str = Column("client name", ignore_case=True)

       # Regex from string
       ref: str = Column(r"^Ref\s*#?\s*\d*$", regexp=True)

       # Compiled regex
       amount: float = Column(re.compile(r"amount", re.IGNORECASE))

       # Callable predicate
       note: str = Column(
           lambda h: h.lower().startswith("note"),
           required=False,
           default="",
       )
