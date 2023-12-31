Newtoki crawling and recommendation
=============

### 목적
한정적인 태그와 검색기능의 한계로 인해 만화를 찾기 어려움을 겪음
확장프로그램이나 앱 개발이 목표
### 문제와 해결방법
* ~~새로운 만화의 업데이트~~ **일주일마다 자동업데이트(8/4)**
* ~~매번 바뀌는 도메인 주소~~ **접속가능한 도메인 주소를 따로 파일로 저장해놓고 업데이트때 읽어서 원활하게 접속(8/5)**
* ~~캡챠~~ ~~**수동 작성(8/8)**~~ **굳이 로그인의 필요성을 못느낌**
* IP차단 **일단 user-agent헤더 추가를 통해 진행하지만 아직 검증되지않아 핫스팟으로 진행중(8/11)**

### 환경
|Python|pip|Selenium|BeautifulSoup4|
|:---:|:---:|:---:|:---:|
|3.11.4|23.2.1|4.11.2|4.12.2|
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
* 10페이지가 안넘어가고 모든 만화를 받을 수 있는 방법을 찾아보니
   1. 요일을 기준으로 진행
  >    
  > 가장 적은 페이지 전환과 아직 페이지의 여유가 있으르모 요일을 기준으로 크롤링하는 것이 좋다고 생각 .. 4471건
  >
   2. ~~초성을 기준으로 진행~~
  >    
  > ~~마찬가지로 한 초성당 10페이지 안으로 있으나 초성들마다 지역성이 있어 추후에는 다른 방법을 찾아야할 가능성이 크다~~

  >!요일기준 검색과 초성기준 검색 결과가 다름 [4471 != 4473] >> 이유 찾는중
  >
  >!요일기준 검색결과 2차 체크 완료 .. *초성기준 검색결과 2차 체크 필요*

* 받아올 정보를 정리해봤다.
  1. 클릭 전
     1. 이미지
     2. 요일
     3. 장르
     4. 제목    
  2. 클릭 후
     1. 별점
     2. 추천
     3. 회차
  3. 그 외
     1. 웹툰 플랫폼
     > '~ 웹툰' 인터넷 검색 > 제일 위에 뜨는거
     > https://blog.zarathu.com/posts/2023-02-15-searchapi-with-python/

- - -
> 8월7일
컨디션 이슈로 인한 휴식

- - -
> 8월 8일
> 구현 시작
* 정리했던 내용들 토대로 크롤링을 진행해봤다.
1. BeautifulSoup4 설치 및 크롤링 시작
   크롤링을 시작해봤다. Selenium은 웹 브라우저를 열고 닫다보니 시간이 오래걸리지만 데이터를 얻기 위해 클릭을 해야하므로 Selenium은 필수불가결했고 페이지에서 데이터를 받아오기에는 BeautifulSoup4가 속도가 빠르므로 두 패키지를 혼합하여 사용하기로 했다.
   !! 생각하니 클릭이벤트가 굳이 필요한가? 요일별로 클릭해놓은 주소를 저장해놓으면 되지 않나?
   !! 들어가도 페이지 넘어가면서 데이터를 받아야하므로 클릭이벤트가 필요할듯하다. == 만약 이 페이지들도 정적으로 저장한다면 추후 웹툰이 추가되어 페이지가 추가될 수 있기 때문이다
   !! 근데 이것도 사실 페이지 갯수를 읽고 저장하면 되지않나? 
   ###### https://deep-flame.tistory.com/27
   
2. ip차단 우회방법
   역시나 크롤링을 하다보니 ip차단이 됐다. 그래서 처음부터 노트북을 핸드폰에서 핫스팟에 연결하고, 차단되면 모바일네트워크를 종료했다 키면 새로운 ip주소를 받아오기 때문에 다시 접속할 수 있게 된다.
   !! 이 방법을 데스크탑 환경에서도 가능하도록 알아봐야겠다.
   !! 크롤링 중간에 차단당하면 멈추기 때문에 지금은 초기단계기 때문에 가능하지만 추후 크롤링할때 차단 안당하도록 알아봐야한다.
   ###### https://daeil.tistory.com/1996
   ###### https://skdrns2.tistory.com/163
   
**!! 문제점**
   1. 일단 가져오고자 하는 데이터가 li태그의 속성값인 것을 알 수 있었지만 이 값을 가져오는 것에 실패했다.
   <img src="\src\뉴토끼_태그속성값데이터.png"></img>
   2. 체력때문에 생각보다 오래 집중할 수 없었다. 빠른 건강회복이 필요할듯 하다.
- - -
> 8월 9일 ~ 8월 10일
>
* 뭉뚱그려서 작성해서 그렇지만 이틀동안 1. 컨디션 회복은 기본으로 2. 크롤링 강의 2편을 완강했다.
* 최근 비가 와서 3. 긴급 집안일 + 집에서 인터넷을 하다보니 느려서 시간이 오래걸렸다.
  
**!! 문제점**
   1. 핑계다. 
- - -
> 8월 11일
>
1. 속성값 추출에 성공.
??왜 크롤링이 안됐나 했는데 **목적 페이지가 동적 페이지였기 때문에** 정적인 url로 바로 들어가면 안됐고, Selenium을 통해 동적으로 이동(click event)하여 데이터를 페이지를 받아오도록 했다. >> 이유를 몰라 한참 걸렸고 그 와중에 아이피 차단 당해서 시간이 더 걸렸다. 또 Selenium과 BeautifulSoup을 병행하면서 진행하다보니 사용법이 헷갈리기도 했다.
2. 데이터 구조 작성
데이터 구조를 작성해야겠다. 데이터를 어떻게 받을지 생각해보니 지금은 각 장르마다 테이블을 만드는게 최우선 같다. 만약 여러 장르를 가지고 있다면 여러테이블에 있도록.
아니면 테이블을 받아올 정보마다 만드는 건 어떨지 생각해보자.
마지막으로 MySQL과 연동도 해야하므로 저장은 엑셀로 하되 최대한 MySQL양식에 맞게 저장하자
* ###### https://zionh.tistory.com/44 엑셀-MySQL연동
3. 엑셀 저장
일단 임시로 엑셀에 데이터를 저장해봤다. 엑셀에서 따로 저장한 url을 읽어와서 webdriver를 실행시키고 만약 사이트가 변동됐다면 해당 숫자에서 1씩 더하면서 새로 접속을 시도한다. 접속이 되면 접속가능한 url을 덮어쓴다.
4. 페이지 이동
마찬가지로 동적페이지기 때문에 Selenium을 이용해 클릭을 진행한 뒤 데이터를 모았다. 물론 반복문을 사용해야했지만 지금은 다음페이지에서 단순히 데이터를 잘읽었느냐만 확인했다. 첫페이지에서 데이터를 잘 받아온줄 알았더니 request할때 변동된 주소(driver.current_url)을 안넣고 초기주소(url)만 넣어서 모든 데이터를 긁어오지 못했다. 이것 때문에 시간이 또 오래 걸렸다.

**!! 문제점**
   1. 예전에 해봤던 프로젝트인데 너무 시간이 오래걸린다. 정신차리고 집중하자
   2. ip차단에 대해서 아직 완벽하게 해결되지 않았다. 빨리 완성하고 핫스팟 대신 인터넷망을 사용해 시간을 줄여보자
   3. 데이터베이스 강의를 찾아보고 적절한 설계를 해보자
   4. 페이지 읽는걸 반복문으로 하자.

- - -
> 8월 31일
>

**!! 왜 아팠나 했더니 코로나였다.**
실제로 아팠던건 2주 정도 8월 14일~8월 28일
그 이후 2일은 회복 느낌으로 좀 쉬었다.
회복 기간이 너무 길었던게 문제다.
8월 13일에 해놓은 작업이 있는데 노트북을 확인해보고 가까운 시일 내에 업로드하도록 하겠다.
코로나 진짜 아프다

> 9월 14일
>

1. 근황
   
   코딩을 하다 생기는 문제점을 바로 주석으로 적어놓고 해결하고 그러는 과정에서 README업데이트가 늦어졌다.
예상했던 기간 한달(코로나기간 제외)보다 시간이 더 걸리는 것을 봐서 얼마나 게을리 했는지 알 수 있었다. << 반성이 필요하다.

2. 한계점 파악
하다보니 내 한계점을 파악할 수 있었다. 그리고 앞으로 더 나은 생활을 위해 적어놓기로 한다.
> 집중 예열 시간 : 2시간
>> 시작시간을 애초에 2시간 일찍해버리자. ex) 보통 1시에 공부하러 나와서 3시부터 시작하므로 아싸리 11시에 나와버리자
> 
> 집중 유지 기간 : 3일
>> 프로젝트를 한개만 하지말고 여러개를 해버리자. 하나에 흥미 식으면 다른 프로젝트를 진행하는 식으로
>      
> 집중 유지 시간 : 3시간
>> 솔직히 더 늘릴 자신이 없다. 그래서 그 집중시간동안 효율적인 결과를 내기위해 내용정리를 잘해야겠다. 한번 배웠던 내용을 정리해서 다음에 같은 내용이 나왔을 때 다시 검색해서 찾는 것보단 이미 정리된 내용에서 찾아쓰는게 훨씬 시간이 덜 걸릴 것 같다.
> 
> 재집중 시간 : 30분
>> 이건 최대한 줄여보도록 노력할 것이고, 그 휴식시간동안 영상이나 게임같은건 안하고 음악감상, 산책으로 대체하여 더 시간쓰지 않도록 조절해야겠다.
> 
> 음악 집중 절대안됨
>> 이 README를 쓰면서도 집중이 안되는데 개발이나 공부에는 얼마나 도움이 안될까. 화이트노이즈, 클래식 이런 것들도 의미없다. 그냥 아무것도 없이 집중해야한다. 겸업으로 단순 숫자계산 작업이나 가능하지 나한테는 머리 조금이라도 써야하는 작업할 때는 안된다는 것을 알았다.

**!! 문제점과 해결 !!**
코드에 있는 문제점/해결 주석을 일단 옮겨와봤다. ( #!! : 문제점 / #~~ : 해결 )
1. crawling.py ( first_page(url,w) )
   
   1.1 매개변수(w)를 알기 쉽게 변환하자.. '월요일' 이런식으로 어떤 요일을 크롤링할지 알면 좋을 것 같다.
   
   1.2 ~~Selenium으로 실행하면 안되지만 실제 웹브라우저에서 실행하면 되는 현상이 있다~~ 다음날 주소가 변경되었다. (307->308) url이 바뀌는 타이밍에 크롤링 시도하면 안되는것 같다?
   
   1.3  ~~핫스팟으로는 되는데 다른 공유와이파이로는 안됐다. 오히려 빨라서 안되는것 같다.~~ 그냥 time.sleep(2)을 줬다.
   
   1.4 ~~page수 가져오는 것 Selenium보다 Request 쓰자~~ 사실 별 차이없는 것 같지만 일단 수정했다.


2. crawling.py ( page_crawl(update_num, week_num, p) )

   2.1 매개변수(week_num) 정리 위와 동일
   
   2.2 상세페이지 url 가져오는 것 Request 쓰자
   
   2.3 ~~이미지 중복저장을 막기위해 이미지 url도 저장하자~~ 나중에 업데이트부분도 만들건데 거기서 웹툰제목으로 중복처리를 할 것이라서 굳이 안해도 이미지 중복저장은 되지 않을 것이다.
   
   2.4 ~~이미지도 배율이 달라서 그냥 상세페이지에서 다루자~~ detail_page로 이전완료


3. crawling.py ( captcha() )
   3.1 캡챠입력이 틀렸을 때 예외처리
   
   3.2 ~~캡챠 이미지 다운받아서 출력해주면 driver 옵션에 headless를 추가하여 속도를 올릴수 있을 것이다~~ 캡챠 이미지 다운이 막히는 것 같으니 driver에서 화면자체를 캡쳐해서 진행했다.
   
   3.3 ~~driver에서는 캡챠인증이 되어 요소를 받을 수 있는데 request에선 캡챠가 안뚫린다~~ Session에서 쿠키를 업데이트 함으로써 뚫었음
   
   3.4 ~~이미 쿠키가 업데이트된 경우 예외처리~~ 처리완료
   
   3.5 현재 plt와 pyautogui를 활용하여 이미지 출력과 입력을 받고 있는데, 동시에 나오게 하는 방법이 있거나 한 프로그램으로 두 기능 실행할 수 있는지 확인해야한다.
   

4. crawling.py ( detail_page(i, cookie) )
   
   4.1 모든 작업이 request로 진행하다보니 ip차단이 걸리는 부분이다. User-Agent를 해도 차단당하므로 IP주소를 바꾸고 실행 속도를 조절하면서 피해봐야겠다.
   ##### https://blog.hashscraper.com/5-principles-for-bypassing-web-crawling-blocks/

   4.2 중간에 ip차단 되면 어떤 웹툰부터 됐는지 시간이 언젠지 기록해놓자. 보통 공용와이파이는 2시간마다 ip가 바뀐다고 한다.

   
5. create_excel
   5.1 추후 작업을 편하게 하기 위해 csv파일로 저장해야하는데 xlsx파일로 저장했다. 나중에 csv파일로 바꾸자 (모든 코드를 수정해야하므로 마지막에 하자)

> 9월 19일
>
1. 최종목표 선택해야함

내가 이걸 함으로써 궁극적으로 만들고 싶은 것? >> 앱으로 만들지 / 웹페이지로 만들지 / 아님 웹앱으로 만들지 / 아님 다른 프로그램으로 만들지
: 내가 봤을 땐 핸드폰으로도 많이 보니까 최종적으로는 앱이 맞는 것 같다.
웹툰들에 대해서 불법 사이트말고 어디서 볼 수 있는지 확인해보자. ( ~ 웹툰 이라고 검색했을 때 가장 상위에 나오는 "네이버시리즈" "카카오페이지" "탑툰" 등을 검색하면 될듯 )
~~이미지 파일에 대해서 MySQL에 직접 저장을 할지 아니면~~ 그냥 내 로컬컴퓨터를 서버로 해서 여기서 운용할지 고민 (184MB정도 되서) 근데 이럼 핸드폰에 이미지 파일을 저장하게 되는건가? 공부가 필요할 것 같다
데이터베이스 설계도 한번 짜보자


