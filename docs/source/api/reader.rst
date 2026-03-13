.. _api-reader:

Reader
======

The top-level reading functions. Both are available directly from the
``xlea`` namespace.

.. code-block:: python

   import xlea
   xlea.read(...)
   xlea.autoread(...)

.. autofunction:: xlea.read

.. autofunction:: xlea.autoread

----

Errors raised at the call site
-------------------------------

Both functions resolve the schema header **eagerly** — before any row is
yielded. This means schema errors surface immediately, not during iteration:

.. code-block:: python

   from xlea.exc import HeaderNotFound

   try:
       rows = xlea.autoread("data.xlsx", schema=MySchema)
   except HeaderNotFound:
       print("Could not find the required columns in this file.")
