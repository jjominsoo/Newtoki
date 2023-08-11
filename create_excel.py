import openpyxl

wb = openpyxl.Workbook()
url = wb.create_sheet('URL')
url['A1'] = 'URL'
url['A2'] = "https://newtoki301.com"


week = wb.create_sheet('요일')
week['A1'] = '월요일'
week['B1'] = '화요일'
week['C1'] = '수요일'
week['D1'] = '목요일'
week['E1'] = '금요일'
week['F1'] = '토요일'
week['G1'] = '일요일'
week['H1'] = '열흘'



wb.save(r'C:\Users\jjomi\PycharmProjects\NewtokkiCrawling\src\Newtoki.xlsx')
