Newtoki crawling and recommendation
=============

### 목적
단일화된 검색과 유저 취향에 맞는 만화 추천

### 문제와 해결방법
* ~~새로운 만화의 업데이트~~ **일주일마다 자동업데이트**
* ~~매번 바뀌는 도메인 주소~~ **접속가능한 도메인 주소를 따로 파일로 저장해놓고 업데이트때 읽어서 원활하게 접속**

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

<img src="./system_interpreter.png"></img>
###### why? 내 컴퓨터에 설치된 패키지들은 파이참의 인터프리터는 인식하지 못하므로 내 컴퓨터에 있는 인터프리터를 사용해야한다.

- - -
> 8월 5일
>
