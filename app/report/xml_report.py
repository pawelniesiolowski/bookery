"""Service for generating books statistics in XML format"""


import io
from typing import List, Dict
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font


class XmlBooksReport():
    def __init__(self) -> None:
        self.workbook = Workbook()
        self.sheet = self.workbook.active

    def prepare(self, books: List[Dict]) -> None:
        self.configure_column_dimensions()
        self.create_header()
        self.create_body(books)

    def save(self, output: io.BytesIO) -> None:
        self.workbook.save(output)

    def create_header(self) -> None:
        header_font = Font(bold=True, size=13)

        self.sheet['A1'] = 'Lp'
        self.sheet['A1'].font = header_font

        self.sheet['B1'] = 'Tytuł'
        self.sheet['B1'].font = header_font

        self.sheet['C1'] = 'ISBN'
        self.sheet['C1'].font = header_font

        self.sheet['D1'] = 'Cena'
        self.sheet['D1'].font = header_font

        self.sheet['E1'] = 'Liczba egzepmlarzy'
        self.sheet['E1'].font = header_font

        self.sheet.row_dimensions[1].height = 20

    def create_body(self, books: List[Dict]) -> None:
        for i, book in enumerate(books):
            num = i + 2
            row = str(num)
            ord_num = i + 1

            alignment = Alignment(horizontal='left')

            self.sheet['A' + row] = ord_num
            self.sheet['A' + row].alignment = alignment

            self.sheet['B' + row] = book['title']
            self.sheet['B' + row].alignment = alignment

            self.sheet['C' + row] = book['isbn']
            self.sheet['C' + row].alignment = alignment

            self.sheet['D' + row] = book['price']
            self.sheet['D' + row].alignment = alignment

            self.sheet['E' + row] = book['copies']
            self.sheet['E' + row].alignment = alignment

            self.sheet.row_dimensions[num].height = 20

    def configure_column_dimensions(self) -> None:
        self.sheet.column_dimensions['A'].width = 10
        self.sheet.column_dimensions['B'].width = 80
        self.sheet.column_dimensions['C'].width = 30
        self.sheet.column_dimensions['D'].width = 10
        self.sheet.column_dimensions['E'].width = 20
