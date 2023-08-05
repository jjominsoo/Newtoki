Newtoki crawling and recommendation
=============

### 목적
한정적인 태그와 검색기능의 한계로 인해 만화를 찾기 어려움을 겪음

### 문제와 해결방법
* ~~새로운 만화의 업데이트~~ **일주일마다 자동업데이트(8/4)**
* ~~매번 바뀌는 도메인 주소~~ **접속가능한 도메인 주소를 따로 파일로 저장해놓고 업데이트때 읽어서 원활하게 접속(8/5)**

### 환경
|Python|pip|Selenium|
|:---:|:---:|:---:|
|3.11.4|23.2.1|4.11.2|
- - -
> 8월4일
>
#### 1. 파이썬 환경변수 설정과 패키지 설치
* pip install --update pip
* pip install (--update) selenium
* pip install (--update) webdriver_manager

?? 셀레니움 참조가 안됨

#### 2. 파이참 인터프리터 설정
* File > Settings > 톱니바퀴 Add > System Interpreter > 컴퓨터에 설치된 파이썬.exe 경로
<img src="\src\system_interpreter.png"></img>
###### why? 내 컴퓨터에 설치된 패키지들은 파이참의 인터프리터는 인식하지 못하므로 내 컴퓨터에 있는 인터프리터를 사용해야한다.

- - -
> 8월 5일
>
#### 1. github readme 작성
어제 몫까지 작성

#### 2. git 업로드
노트북으로 작업했기 때문에 데스크탑에 옮기기 위해서 git을 사용
> 노트북
>> cd (작업한폴더 : ~\NewtokkiCrawling)
>> 
>> git config --global user.email jjominsoo987@naver.com
>>
>> git config --global user.name jjominsoo
>> 
>> git init
>>
>> git add *
>>
>> git commit -m "message"
>>
>> git remote add origin https://github.com/jjominsoo/Newtoki.git .. origin이라는 이름으로 저장하겠다는것
>> 
>> git push origin master .. master란 브랜치에 저장하겠다는것

> 데스크탑
>> git bash 실행
>>
>> git clone https://github.com/jjominsoo/Newtoki.git
