# temp = "av,d,se,scds"
#
# a = []
# a = temp.split(',')
# print(a)
#
# b = []
# cell_alp = ['F','G','H','I','J','K','L','M','N','O','P','Q','R']
# cell_alp2 = {'판타지':'F','액션':'G','개그':'H','미스터리':'I','로맨스':'J','드라마':'K','무협':'L','스포츠':'M','일상':'N','학원':'O','성인':'P','한국':'Q','중국':'R'}
#
# genre = ['판타지','미스터리','스포츠','중국']
# s = 2
# for i, g in enumerate(genre):
#     if g in cell_alp2.keys():
#         b.append(cell_alp2[g] + '%d'%s)
#     s += 1
#
# print(b)
#
# week = ['월요일','화요일','수요일','목요일','금요일','토요일','일요일','열흘']
# for w in range(1, len(week)):
#     print(week[w])

# import re
# a = "a s d b dd 아?"
# b = re.sub(r"[^\uAC00-\uD7A30\s]","",a)
# print(b)

# <<<<<<< HEAD
# total_time = 4535
#
# hour = total_time//3600
# min = (total_time - 3600*hour)//60
# second = total_time%60
# print(hour, min,second)
#
# recommend_num = '1,113'
# recommend_num = recommend_num.replace(",", "")
# print(int(recommend_num))

# import shutil
# i = 0000000
# temp_img = "src/files/no_image.png"
# img = f'src/files/{i}.png'
# shutil.copyfile(temp_img,img)

# for i in range(2,10):
#     print(i)
# # =======
# total_time = 4535
#
# hour = total_time//3600
# min = (total_time - 3600*hour)//60
# second = total_time%60
# print(hour, min,second)
#
# recommend_num = '1,113'
# recommend_num = recommend_num.replace(",", "")
# print(int(recommend_num))
# >>>>>>> 2b8f3df3de3f3e63702947fcfb1bfe7c0ec4725e

# webtoon_first_url = "https://newtoki307.com/webtoon/438868?sst=as_update&sod=desc&yoil=%EC%9B%94&toon=%EC%9D%BC%EB%B0%98%EC%9B%B9%ED%88%B0"
# print(len(webtoon_first_url))
#
# webtoon_genre = ['무협','중국']
# a = ",".join(webtoon_genre)
# print(a)
# for genr?e in webtoon_genre:

import os

if os.path.getsize("src/files/bookmark.txt") <= 0:
    f2 = open("src/files/bookmark.txt",'w',encoding='utf8')
    f2.write("0\n")
    f2.write("\n")
    f2.write("\n")
    print("hemllod")
    f2.close()
# with open("src/files/bookmark.txt",'r',encoding="utf8") as f3:
#     ## bookmark.txt에는 웹툰번호 / 여태저장한 리스트 가 저장될 것이다.
#     a = f3.readlines()
#     k = int(a[-2].strip("\n"))
#     k2 = a[-1].strip("\n")
#     if len(k2) > 0:
#         k3 = k2.split(".")
#     else:
#         k3 = []
#     print(k)
#     print(k2)
#     print(k3)
#
#     f2 = open("src/files/bookmark.txt", 'w', encoding='utf8')
#
#     l = 2
#     l2 = ["탑툰,카카오웹툰","카카오웹툰,레진코믹스,네이버웹툰"]
#     f2.write(str(k+l)+"\n")
#     f2.write(".".join(k3 + l2))
#     f2.close()
#
#     f4 = open("src/files/bookmark.txt", 'r', encoding='utf8')
#     print(f4.read())
# print(last_num)
# print(last_webtoon_source)