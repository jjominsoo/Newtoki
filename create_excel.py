import openpyxl
from datetime import datetime


wb = openpyxl.Workbook()
info = wb.create_sheet('Site Information')
info['A1'] = 'URL'
info['A2'] = "https://newtoki306.com"
info['B1'] = 'Last Update'
info['B2'] = datetime.now()
info['C1'] = 'Update List'
info['D1'] = 'Recent Webtoon Number'
info['D2'] = 2

week = wb.create_sheet('webtoon')
week['A1'] = '이름'
week['B1'] = '이미지'
week['C1'] = '추천수'
week['D1'] = '별점수'
week['E1'] = '총화수'
week['F1'] = '판타지'
week['G1'] = '액션'
week['H1'] = '개그'
week['I1'] = '미스터리'
week['J1'] = '로맨스'
week['K1'] = '드라마'
week['L1'] = '무협'
week['M1'] = '스포츠'
week['N1'] = '일상'
week['O1'] = '학원'
week['P1'] = '성인'
week['Q1'] = '한국'
week['R1'] = '중국'
week['S1'] = '요일'
week['T1'] = '1화링크'
week['U1'] = '최신화링크'
week['V1'] = '상세페이지 URL'

wb.save(r'C:\Users\jjomi\PycharmProjects\NewtokkiCrawling\src\Newtoki.xlsx')
