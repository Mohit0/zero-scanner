#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import xlsxwriter
import bs4
import json 
  
name = input("Enter name of file to convert to Excel: ")
f = open(name, encoding='utf-8')

data = json.load(f)

# Creating workbook with all columns
workbook = xlsxwriter.Workbook('xls_result.xlsx')
worksheet = workbook.add_worksheet()

values = ['Risk ID', 'Vulnerability Name', 'Affected Instances', 'Description', 'Impact', 'High Level Fix Recommendation', 'Final Risk', 'Status SA Spoc', 'Finding Date']

for col in range(9):
    worksheet.write(1, col, values[col])

worksheet.write(0,0, str(data['name'] + " - " + data['company']['name']))

count = len(data['findings'])
for i in range(count):
    worksheet.write(i + 2, 0, i + 1)
    worksheet.write(i + 2, 1, str(data['findings'][i]['title']))
    worksheet.write(i + 2, 2, str(data['findings'][i]['scope']))
    worksheet.write(i + 2, 3, str(data['findings'][i]['description']))
    worksheet.write(i + 2, 4, str(data['findings'][i]['customFields'][0]['text']))
    worksheet.write(i + 2, 5, str(data['findings'][i]['remediation']))
    worksheet.write(i + 2, 6, str(data['findings'][i]['cvssSeverity']))
    worksheet.write(i + 2, 7, "N/A")
    worksheet.write(i + 2, 8, str(data['date_end']))
    
f.close()
workbook.close()

