import pymysql
import pandas as pd


webtoon_name = "절세무신"
webtoon_recommend = 72
webtoon_star = 2.5
webtoon_num = 341
webtoon_genre = ['무협','중국']
genre = ",".join(webtoon_genre)
webtoon_day = "월요일"
webtoon_first_url = 'https://newtoki307.com/webtoon/438868?sst=as_update&sod=desc&yoil=%EC%9B%94&toon=%EC%9D%BC%EB%B0%98%EC%9B%B9%ED%88%B0'
webtoon_url = 'https://newtoki307.com/webtoon/438864/%EC%A0%88%EC%84%B8%EB%AC%B4%EC%8B%A0?sst=as_update&sod=desc&yoil=%EC%9B%94&toon=%EC%9D%BC%EB%B0%98%EC%9B%B9%ED%88%B0'

fpath = r'C:\Users\jjomi\PycharmProjects\NewtokkiCrawling\src\Newtoki_webtoon2.csv'
df =pd.read_csv(fpath)

# print(df.loc[0])
# print(len(df))
# print(df.loc[4513]['이름'])



conn = pymysql.connect(host='127.0.0.1', user='root', password='whalstn971230!', db='newtoki', charset='utf8')
cur = conn.cursor()

cur.execute("drop table if exists temp")
cur.execute("CREATE TABLE temp (name CHAR(60), recommend SMALLINT, star FLOAT, totalNum SMALLINT, genre CHAR(50), day CHAR(20), firstURL VARCHAR(2048), URL VARCHAR(2048))")
for i in range(len(df)):
    try:
        print(df.loc[i]['이름'])
        cur.execute(f"INSERT INTO temp VALUES(\"{df.loc[i]['이름']}\" , {df.loc[i]['추천수']} , {df.loc[i]['별점수']} , {df.loc[i]['총화수']} , \"{df.loc[i]['장르모음']}\" , \"{df.loc[i]['요일']}\" , \"{df.loc[i]['1화링크']}\" , \"{df.loc[i]['상세페이지 URL']}\")")
    except:
        print(i)
        a = input()
conn.commit()
conn.close()