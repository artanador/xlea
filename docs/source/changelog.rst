.. _changelog:

Changelog
=========

All notable changes to xlea are documented here.

.. rubric:: 1.0.2 — 2026-03-13

**Bug fix:** `HeaderNotFound` raised lazily instead of eagerly
(`#3 <https://github.com/artanador/xlea/issues/3>`_)

When calling ``read()`` or ``autoread()`` with a schema, the
:exc:`~xlea.exc.HeaderNotFound` exception was not raised immediately — it
was deferred until the caller started iterating over the returned generator.
This made error detection unpredictable and violated the principle of least
surprise.

Schema resolution is now **eager**: :exc:`~xlea.exc.HeaderNotFound` (and its
subclass :exc:`~xlea.exc.MissingRequiredColumns`) are raised at the
``read()`` / ``autoread()`` call site, before any iteration begins.

.. code-block:: python

   # Before 1.0.2 — error only surfaced during iteration:
   rows = xlea.autoread("bad.xlsx", schema=MySchema)  # no error yet
   for row in rows:  # HeaderNotFound raised here — surprising!
       ...

   # After 1.0.2 — error raised immediately:
   rows = xlea.autoread("bad.xlsx", schema=MySchema)  # HeaderNotFound here ✓

Additional changes in this release:

- Added ``.xlsm``, ``.xltx``, ``.xltm`` extensions to the openpyxl provider registry
- Providers now import their dependencies lazily and raise
  :exc:`~xlea.exc.ProviderError` with a helpful install hint on ``ImportError``
- :exc:`~xlea.exc.MissingRequiredColumns` added as a subclass of
  :exc:`~xlea.exc.HeaderNotFound` — includes the names of the missing columns
  in the error message
- :exc:`~xlea.exc.IncompatibleReturnValueTypeError` raised when a validator
  returns a non-``bool`` value
- ``BoundSchema`` header search is now streaming — no longer buffers all rows
  into a tuple upfront

----

.. rubric:: 1.0.1

**Bug fix:** ``IndexError: tuple index out of range`` on empty rows
(`#1 <https://github.com/artanador/xlea/issues/1>`_)

Some Excel providers (openpyxl, xlrd) emit an empty tuple ``()`` for blank
rows in a spreadsheet instead of skipping them. Before this fix, xlea
attempted to access an index on that empty tuple and raised an uncaught
``IndexError``.

Empty rows are now **normalised** automatically: they are padded with
``None`` values to match the required column width and passed through the
normal validation pipeline — either skipped (if ``skip_invalid_row=True``)
or handled as any other row with missing values.

.. code-block:: python

   # Before 1.0.1:
   for row in xlea.autoread("file_with_blank_rows.xlsx", schema=MySchema):
       print(row.id)  # IndexError on blank row ✗

   # After 1.0.1:
   for row in xlea.autoread("file_with_blank_rows.xlsx", schema=MySchema):
       print(row.id)  # blank rows handled gracefully ✓

----

.. rubric:: 1.0.0

Initial public release.

- Declarative schema definition via :func:`~xlea.Column` descriptors
- Automatic header detection (position-independent)
- Type conversion driven by annotations
- Multi-row header support via ``@config(header_rows=N)``
- Built-in providers: :class:`~xlea.providers.openpyxl.OpenPyXlProvider`,
  :class:`~xlea.providers.xlrd.XLRDProvider`,
  :class:`~xlea.providers.pyxlsb.PyXLSBProvider`
- :func:`~xlea.register_provider` for custom file extensions
- Per-column validators with ``skip_invalid_row`` support
