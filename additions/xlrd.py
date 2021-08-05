#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import xlrd
import docx


loc = "file.xls"

wb = xlrd.open_workbook(loc, encoding_override="gb2312")
sheet = wb.sheet_by_index(0)
sheet.cell_value(0, 0)
rows = sheet.nrows

print("\n")

print("Sheet has" + str(rows) + "rows.\n")

for i in range(rows):
    i=i+1

    # HASHTAG
    text = str(sheet.cell_value(i, 2)))
    print(text)
    #doc.add_paragraph(text)

#doc.save("file.docx")sssssss