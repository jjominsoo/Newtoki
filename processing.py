import numpy
import os
import openpyxl
import csv
import time
import pandas as pd
from openpyxl.drawing.image import Image as XLImage
from PIL import Image
fpath = r'C:\Users\jjomi\PycharmProjects\NewtokkiCrawling\src\Newtoki7.xlsx'
c = open('src/Newtoki.csv','w')
wc = csv.writer(c)

# xls = pd.ExcelFile(fpath)
# df = xls.parse(xls.sheet_names[2])
# df2 = xls.parse(xls.sheet_names[1])
df = pd.read_excel(fpath,sheet_name=2)
df2 = pd.read_excel(fpath,sheet_name=1)
df3 = df2['Update List']


wb = openpyxl.load_workbook(fpath)
wb_siteInfo = wb['Site Information']
wb_webtoon = wb['webtoon']

# 총 화수가 0이면 그냥 추가하지말자
# 이미지도 지우고
# site_info 수정도 잊지말고
# 엑셀에서 행을 지워버리고 위로 정렬하는것도 좋아보임
def delete_nothing():
    delete_row = []
    for i, row in enumerate(df['총화수']):
        if row == 0:
            # print(df.loc[i]['이름'])
            delete_row.append(i)
            # print(df2.loc[i]['Update List'])
    df.drop(['이미지'],axis=1,inplace=True)
    df.drop(delete_row,axis=0,inplace=True)
    df3.drop(delete_row,axis=0,inplace=True)

delete_nothing()

# df.to_excel(fpath)

new_df = df.to_csv("src/Newtoki_webtoon.csv",sep=",",index=False)
new_df3 = df3.to_csv("src/Newtoki_update.csv",sep=",",index=False)


# 일단 확실하게 이름 저장된 부분 (site_information)은 따로 csv파일로 저장하는거고




# print(df)
# print(len(df['총화수']))



# 이미지 엑셀 저장 파트
# 이미지는 크롤링 개념이 아니라 이미 다운받은 파일을 삽입하는 과정이므로 따로 구현했다.
#!! 지금보니 나중에 DB로 합칠땐 이미지 부분이 필요가 없다 >> 서버(데스크탑)에 저장해놓고 사용하니깐
# def save_image_to_excel():
#     img_dir = 'src/img/'
#     no_img_dir = 'src/files/'
#     img_file_list = sorted(os.listdir(img_dir), key=lambda x: int(x.split('.')[0]))
#     for i, img_file in enumerate(img_file_list):
#         try:
#             # print("Starting Resizing..")
#             image_path = os.path.join(img_dir, img_file)
#             img_resize = Image.open(image_path).resize((150,150))
#             # print("Resizing End! .. saving...")
#             img_resize.save(image_path,"PNG",quality=95)
#             image = XLImage(image_path)
#             wb_webtoon.add_image(image, anchor='B' + str(i + 2))
#         # 물론 처음 상세페이지에서 크롤링할때 대표 이미지가 없다면 대신할 이미지를 저장했지만 그 조차도 0과 null의 차이가 있어서 한번더 진행해야했다.
#         except Exception as e:
#             print(e, end="")
#             print(i)
#             image_path = os.path.join(no_img_dir, 'no_image.png')
#             img_resize = Image.open(image_path).resize((150, 150))
#             img_resize.save(image_path, "PNG", quality=95)
#             image = XLImage(image_path)
#             wb_webtoon.add_image(image, anchor='B' + str(i + 2))
#         if i == 0:
#             wb_webtoon.column_dimensions['B'].width = image.width * 63.2 / 504.19
#         wb_webtoon.row_dimensions[i + 2].height = image.height * 225.35 / 298.96
#
#     wb.save(fpath)
# save_image_to_excel()