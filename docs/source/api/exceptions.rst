.. _api-exceptions:

Exceptions
==========

All exceptions inherit from :exc:`XLEAError`, making it easy to catch
any xlea error with a single ``except`` clause.

Hierarchy
---------

.. code-block:: text

   XLEAError
   ├── ProviderError
   ├── HeaderNotFound
   │   └── MissingRequiredColumns
   ├── InvalidRowError
   ├── UnknownFileExtensionError
   └── IncompatibleReturnValueTypeError

Reference
---------

.. autoexception:: xlea.exc.XLEAError

.. autoexception:: xlea.exc.ProviderError

.. autoexception:: xlea.exc.HeaderNotFound

.. autoexception:: xlea.exc.MissingRequiredColumns

.. autoexception:: xlea.exc.InvalidRowError

.. autoexception:: xlea.exc.UnknownFileExtensionError

.. autoexception:: xlea.exc.IncompatibleReturnValueTypeError

----

Error handling example
----------------------

.. code-block:: python

   import xlea
   from xlea.exc import (
       HeaderNotFound,
       MissingRequiredColumns,
       InvalidRowError,
       UnknownFileExtensionError,
       XLEAError,
   )

   try:
       for row in xlea.autoread("report.xlsx", schema=MySchema):
           process(row)

   except MissingRequiredColumns as e:
       # More specific: tells you exactly which columns are missing
       print(f"File is missing columns: {e}")

   except HeaderNotFound:
       print("Could not locate the header row in this file.")

   except InvalidRowError as e:
       print(f"A data row failed validation: {e}")

   except UnknownFileExtensionError:
       print("File format not supported. Install the right extra.")

   except XLEAError as e:
       # Catch-all for any xlea error
       print(f"xlea error: {e}")
