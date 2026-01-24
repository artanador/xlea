import xlea
from xlea import Schema, Column
from xlea.providers.openpyxl import OpenPyXlProvider


class Person(Schema):
    id = Column("ID")
    fullname = Column("фио", ignore_case=True)
    age = Column("Возраст")
    city = Column("Город", required=False, default="Воронеж")


def main():
    persons = xlea.read(OpenPyXlProvider("examples/test_data.xlsx"), schema=Person)
    for p in persons:
        print(p.asdict())
        print(p.city)
        print(p.age)


if __name__ == "__main__":
    main()
