#!/usr/bin/python3

from openpyxl import Workbook

def createExcel():
    book = Workbook()
    sheet = book.active

    rows = (
        (34, 26),
        (88, 36),
        (24, 29),
        (15, 22),
        (56, 13),
        (76, 18)
    )
    print type(rows), type(rows[1])

    # for row in rows:
    #     sheet.append(row)

    # cell = sheet.cell(row=7, column=2)
    # cell.value = "=SUM(A1:B6)"
    # #cell.font = cell.font.copy(bold=True)

    # book.save('formulas.xlsx')

createExcel()