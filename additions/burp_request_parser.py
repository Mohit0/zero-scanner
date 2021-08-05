#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import xlsxwriter
import bs4

name = input("Enter name of file to convert to Excel: ")
try:
    f = open(name)
    doc_xml = bs4.BeautifulSoup(f, 'xml')
    host = [el.text for el in doc_xml.findAll('host')]
    protocol = [el.text for el in doc_xml.findAll('protocol')]
    port = [el.text for el in doc_xml.findAll('port')]
    httpmethod = [el.text for el in doc_xml.findAll('method')]
    urls = [el.text for el in doc_xml.findAll('url')]
    request = [el.text for el in doc_xml.findAll('request')]
    status = [el.text for el in doc_xml.findAll('status')]
    response = [el.text for el in doc_xml.findAll('response')]
    path = [el.text for el in doc_xml.findAll('path')]

    # Creating workbook with all columns
    workbook = xlsxwriter.Workbook('burp_result.xlsx')
    worksheet = workbook.add_worksheet()

    values = ['S.no', 'Host', 'Protocol', 'Port', 'Method', 'URL(s)', 'Request', 'Response Code', 'Response', 'Path']
    for col in range(10):
        worksheet.write(0, col, values[col])

    for i in range(len(urls)):
        worksheet.write(i + 1, 0, i + 1)
        worksheet.write(i + 1, 1, str(host[i]))
        worksheet.write(i + 1, 2, str(protocol[i]))
        worksheet.write(i + 1, 3, port[i])
        worksheet.write(i + 1, 4, str(httpmethod[i]))
        worksheet.write(i + 1, 5, str(urls[i]))
        worksheet.write(i + 1, 6, str(request[i]))
        worksheet.write(i + 1, 7, str(status[i]))
        worksheet.write(i + 1, 8, str(response[i]))
        worksheet.write(i + 1, 9, str(path[i]))
    workbook.close()

except Exception as e:
    print("Error occured:\n Trace:" + str(e))

