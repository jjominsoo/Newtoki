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

for i in range(2,10):
    print(i)