Newtoki crawling and recommendation
=============

### 목적
한정적인 태그와 검색기능의 한계로 인해 만화를 찾기 어려움을 겪음
확장프로그램이나 앱 개발이 목표
### 문제와 해결방법
* ~~새로운 만화의 업데이트~~ **일주일마다 자동업데이트(8/4)**
* ~~매번 바뀌는 도메인 주소~~ **접속가능한 도메인 주소를 따로 파일로 저장해놓고 업데이트때 읽어서 원활하게 접속(8/5)**
* ~~캡챠~~ **수동 작성**
* IP차단

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
git 문법을 까먹어서 다시 공부 ./git.md 참고

- - -
> 8월 6일
>
#### 1. 방향성
캡챠, IP차단, 크롤링 후 저장방식 등 여러가지

크롤링 우회
###### https://pythondocs.net/selenium/%EC%85%80%EB%A0%88%EB%8B%88%EC%9B%80-%EC%9B%B9-%ED%81%AC%EB%A1%A4%EB%A7%81-%EB%B4%87-%ED%83%90%EC%A7%80-%EC%9A%B0%ED%9A%8C/

* 캡챠 = ~~번거롭지만 wait()을 걸어서 직접 캡챠번호를 입력한다.~~ 사이트 창을 띄우고 로그인을 한 뒤 셀레니움을 돌리면 된다고 한다.
###### https://domdom.tistory.com/235   
###### https://kissi-pro.tistory.com/entry/%ED%8C%8C%EC%9D%B4%EC%8D%AC-%EC%85%80%EB%A0%88%EB%8B%88%EC%9B%80-%EB%84%A4%EC%9D%B4%EB%B2%84-%EB%A1%9C%EA%B7%B8%EC%9D%B8-%EC%9E%90%EB%8F%99%EC%9E%85%EB%A0%A5-%EB%B0%A9%EC%A7%80%EB%AC%B8%EC%9E%90-%EB%9A%AB%EA%B8%B0#google_vignette .... ~~https://gam860720.tistory.com/532 머신러닝은 과하지않나..~~
* IP차단 = 이 경우 언제 차단 당하는지 모르기 때문에 애매하다. 처음부터 vpn을 키고 작업
###### https://domdom.tistory.com/329
++ https 와 vpn 차이 = https는 dns에서 막는 주소를 구글의 DNS를 통해 사이트를 뚫는 거고(ip변경 X) // vpn은 외국 vpn회사의 서버를 통해 사이트를 대신 뚫어준다.
###### https://kbench.com/community/?q=node/16163
* 저장방식 = 일단 엑셀(csv)로 생각하고 있는데 어차피 도메인 주소도 저장해야하므로 나중엔 MySQL로 저장할 예정

#### 2. 크롤링 진행계획
10페이지가 안넘어가고 모든 만화를 받을 수 있는 방법을 찾아보니
1. 요일을 기준으로 진행
가장 적은 페이지 전환과 아직 페이지의 여유가 있으르모 요일을 기준으로 크롤링하는 것이 좋다고 생각 .. 4471건
~~2. 초성을 기준으로 진행~~
~~마찬가지로 한 초성당 10페이지 안으로 있으나 초성들마다 지역성이 있어 추후에는 다른 방법을 찾아야할 가능성이 크다~~
!요일기준 검색과 초성기준 검색 결과가 다름 4471!=4473 >> 이유 찾는중
!요일기준 검색결과 2차 체크 완료 .. 초성기준 검색결과 2차 체크 필요 >> 

2.2 받아올 데이터  

웹툰 출처 : 쿼리 따서 ~웹툰 인터넷 검색 > 제일 위에 뜨는거
https://blog.zarathu.com/posts/2023-02-15-searchapi-with-python/
