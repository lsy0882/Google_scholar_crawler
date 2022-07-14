# Google_scholar_crawler

## 1. 코드사용 전 설명
* "chrome - 더보기(좌측상단 점3개) - 설정 - Chrome 정보" 에서 현재 pc에 설치된 chrome 버전 확인
* https://chromedriver.chromium.org/downloads 에서 자신에게 맞는 버전의 chromedirver.exe 을 다운로드
   (github에 올린 chromdriver의 버전은 103.0.5060.53)
* 다운로드 받은 chromedriver.exe를 crawling을 진행하는 .py 파일과 동일한 directory로 보냄
* 크롤링간 저장되는 쿠키, 캐쉬 파일을 지우기위해 C:\에 chrometemp 라는 폴더 생성
   (Line 70 에서 커스터마이징 가능)


## 2. 파라미터 설명
(본 코드는 google scholar url에 맞춰져있기 때문에 다른 홈페이지에서 사용하기 위해선 수정이 필요함)
```python
   # 예시)
   parameters = {
       'chromedriver_path' : 'C:/Users/lsy/local_code/Google_scholar_crawler/chromedriver.exe',
       'keyword' : 'IEEE/CVF International Conference',
       'end_page' : 90,
       'from_year' : 2022,
       'result_folder_name' : 'data',
       'excel_name' : 'IEEE_CVF.xlsx',
       'sheet_name' : 'test'
      }
```
* parameters['chromedriver_path'] : chrome.driver.exe 경로를 의미.
* parameters['keyword'] : 구글 스칼라에 검색하고 싶은 내용을 의미.
* parameters['end_page'] : 최대로 Crawling 하고 싶은 페이지 숫자를 의미.
* parameters['from_year'] : 몇년도 이후 논문을 검색할 것인지를 의미. (예시: 2021 -> 2021~현재까지 논문 서칭)
* parameters['result_folder_name'] : crawling 결과를 저장할 폴더명을 의미.
* parameters['excel_name'] : 저장하려는 excel 파일명을 의미.
* parameters['sheet_name'] : 저장하려는 excel 속 sheet 이름을 의미.

## 3. 코드사용 설명
* crawling_scholar.py 속 parameters dictionary를 기호에 맞게 수정 후 run 실시
