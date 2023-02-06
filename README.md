## 네이버 증권 종목토론실 crawler 

네이버 증권 전 종목에서 특정 keyword가 포함되는 게시글의 종목명, 날짜, 제목, 링크를 크롤링해서 엑셀파일로 저장하는 프로그램

### 실행 방법

```
python main.py --keyword KEYWORD --path PATH --schedule SCHEDULE(Optional)
```

- 실행 시 `keyword`, `path`, `schedule`(optional) 세 가지 arguments 전달이 필요
- `keyword`: 검색 단어
- `path`: 엑셀파일을 저장할 디렉토리 path (path 끝에 \\를 필수로 붙여줘야 한다)
- `schedule`: 매일 프로그램을 실행할 시간을 00:00(시:분) 형태로 전달. Ex) 08:00  
  인자를 전달하지 않을 시 한번만 실행하고 종료

```
Example)
python main.py --keyword 관련주 --path C:\\Users\\My\\Desktop\\ --schedule 08:00
```

### 설치해야 할 패키지

```
pip install beautifulsoup4
pip install requests
pip install selenium
pip install openpyxl
pip install pandas
pip install schedule
```

### 추가 설정해야할 부분

#### Selenium

- selenium을 실행시키기 위해 현재 사용하고 있는 크롬 버전에 해당하는 chrome driver 설치가 필요
https://chromedriver.chromium.org/downloads
- driver 실행파일은 `C:/Users/[사용자명]/AppData/Local/Programs/Python/` 에 저장
- crawling.py 42번째 줄의 `executable_path`를 저장한 path에 맞게 수정

#### user-agent

- crawling.py 10번째 줄의 user-agent값을 본인의 user-agent값으로 수정

[user-agent값 확인하기](https://blog.hangyeong.com/1009)