.. _api-providers:

Providers
=========

A provider is responsible for supplying raw rows to xlea. 

Built-in providers
------------------

.. autoclass:: xlea.providers.openpyxl.OpenPyXlProvider
   :members:
   :show-inheritance:

.. autoclass:: xlea.providers.xlrd.XLRDProvider
   :members:
   :show-inheritance:

.. autoclass:: xlea.providers.pyxlsb.PyXLSBProvider
   :members:
   :show-inheritance:

----

Provider registry
-----------------

.. autofunction:: xlea.register_provider

Example — registering a custom CSV provider:

.. code-block:: python

   import csv
   import xlea

   class CSVProvider:
       def __init__(self, path, sheet=None):
           self._path = path

       def rows(self):
           with open(self._path, newline="") as f:
               yield from csv.reader(f)

   xlea.register_provider(".csv", CSVProvider)

   # xlea.autoread now handles .csv files
   for row in xlea.autoread("report.csv", schema=MySchema):
       print(row)

Provider protocol
-----------------

Any object that implements ``rows() -> Iterable[Iterable]`` is a valid
provider — no base class required:

.. autoclass:: xlea.providers.proto.ProviderProto
   :members:
