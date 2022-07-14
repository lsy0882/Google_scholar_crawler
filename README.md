# Google_scholar_crawler

<코드사용 전 설명>
1. 다운로드 받기전에 "chrome - 더보기(좌측상단 점3개) - 설정 - Chrome 정보" 에서 현재 pc에 설치된 chrome 버전 확인
2. https://chromedriver.chromium.org/downloads 에서 자신에게 맞는 버전의 chromedirver.exe 을 다운로드
3. (github에 올린 chromdriver의 버전은 103.0.5060.53)
4. 다운로드 받은 chromedriver.exe를 crawling을 진행하는 .py 파일과 동일한 directory로 보냄
5. 크롤링간 저장되는 쿠키, 캐쉬 파일을 지우기위해 C:\에 chrometemp 라는 폴더 생성
   (Line 61 에서 커스터마이징 가능)


<파라미터 설명>
* 본 코드는 google scholar url에 맞춰져있기 때문에 다른 홈페이지에서 사용하기 위해선 수정이 필요함)
1. Line 14 - parameters['chromedriver_path'] chrome.driver.exe 경로를 자신에게 맞게 수정
2. Line 74 : keyword 변수에 자신이 검색하고 싶은 내용을 기입
3. Line 89 : range() 안에 자신이 최대로 crawling 하고 싶은 페이지 숫자를 기입
4. Line 95 : from_year 변수는 몇년도 이후 논문을 검색할 것인지에 대한 변수이며 원하는 숫자로 기입
5. Line 138 : result_folder_name에 crawling 결과를 저장할 폴더명을 기입
6. Line 139 : excel_name에 자신이 저장하려는 excel 파일명을 기입 (ex: XAI.xlsx)
7. Line 140 : sheet_name_custom에 자신이 저장하려는 excel 속 sheet 이름을 기입 (ex: sheet236)

<코드사용 설명>
* 본 코드는 google scholar url에 맞춰져있기 때문에 다른 홈페이지에서 사용하기 위해선 수정이 필요함)
1. crawling_scholar.py 파일 실행
