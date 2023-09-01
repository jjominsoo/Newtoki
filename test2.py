temp = "av,d,se,scds"

a = []
a = temp.split(',')
print(a)

b = []
cell_alp = ['F','G','H','I','J','K','L','M','N','O','P','Q','R']
cell_alp2 = {'판타지':'F','액션':'G','개그':'H','미스터리':'I','로맨스':'J','드라마':'K','무협':'L','스포츠':'M','일상':'N','학원':'O','성인':'P','한국':'Q','중국':'R'}

genre = ['판타지','미스터리','스포츠','중국']
s = 2
for i, g in enumerate(genre):
    if g in cell_alp2.keys():
        b.append(cell_alp2[g] + '%d'%s)
    s += 1

print(b)

week = ['월요일','화요일','수요일','목요일','금요일','토요일','일요일','열흘']
for w in range(1, len(week)):
    print(week[w])