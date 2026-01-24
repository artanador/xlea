import xlea
from xlea import Schema, Column
from xlea.providers.openpyxl import OpenPyXlProvider


class Person(Schema):
    id = Column("ID")
    fullname = Column("ФИО", ignore_case=True)
    age = Column("Возраст")
    city = Column("город", required=False)


def main():
    persons = xlea.read(OpenPyXlProvider("test_data.xlsx"), schema=Person)

    for p in persons:
        print(p.fullname, p.age, p.id)


if __name__ == "__main__":
    main()
