import xlea
from xlea import Schema, Column
from xlea.providers.openpyxl import OpenPyXlProvider


class Person(Schema):
    id = Column("ID")
    fullname = Column("ФИО")
    age = Column("Возраст")


def main():
    persons = xlea.read(OpenPyXlProvider("examples/test_data.xlsx"), schema=Person)
    for p in persons:
        print(p)


if __name__ == "__main__":
    main()
