Quickstart
==========

Installation
------------

.. code-block:: bash

   pip install xlea

Basic usage
-----------

.. code-block:: python

   from xlea import Schema, Column
   import xlea

   class Person(Schema):
       id: str = Column("ID")
       name: str = Column("Name")

   for person in xlea.autoread("data.xlsx", schema=Person):
       print(person.id, person.name)
