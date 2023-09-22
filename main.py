# library
import sqlite3
from sqlite3 import Error
import sys, requests, time
from bs4 import BeautifulSoup as bs

#input_vendor = input("CVE를 추출하고 싶은 vendor를 고르시오")
input_vendor = "synology"

db_name = "CVE_extract.db"
table_name = "CVE_extract"

base_path = "https://www.opencve.io/cve?vendor=" # + {input_vendor}
target_path = base_path+input_vendor + "&page="
# https://www.opencve.io/cve?vendor=synology&page=2 # 페이지값 추가

def create_db():
    # SQLite 데이터베이스 파일 생성 또는 연결
    conn = sqlite3.connect(db_name)

    # 커서 생성
    cursor = conn.cursor()

    # cve_extract 테이블 생성 쿼리
    create_table_query = """
    CREATE TABLE IF NOT EXISTS cve_extract (
        id_num INTEGER PRIMARY KEY,
        cve_name TEXT,
        vendors TEXT,
        products TEXT,
        update_date TEXT,
        cvss_v2 TEXT,
        cvss_v3 TEXT,
        desc_en TEXT
    );
    """

    # 테이블 생성
    cursor.execute(create_table_query)

    # 변경사항 저장 및 연결 종료
    conn.commit()
    conn.close()
    

# ====
# 1. db를 생성
#create_db()

# 2. cve에 나온 내용 크롤링
total_info = [] # [cve_name, vendors ,products ,update_date ,cvss_v2 ,cvss_v3 ,desc_en]

page_num = 1
total_craw = ''
while True:
    
    page_path = target_path + str(page_num)
    response = requests.get(page_path)
    #print(target_path)
    
    if response.status_code == 200:
        # BeautifulSoup을 사용하여 HTML 파싱
        soup = bs(response.text, 'html.parser')

        # 웹 페이지에서 특정 테이블 선택
        # 웹 페이지의 HTML 구조를 확인하여 실제 표에 해당하는 부분을 선택합니다.
        table = soup.find('table')  # 이 부분을 웹 페이지의 실제 HTML 구조에 맞게 수정하세요.

        # 표의 각 행(row)과 열(column) 순회
        for row in table.find_all('tr'):
            columns = row.find_all('td')
            for column in columns:
                # 각 셀의 내용을 출력하거나 원하는 처리를 수행
                total_craw += "\n"+column.text
                #print(column.text)  # 현재는 텍스트를 출력하는 예제입니다.
    elif response.status_code == 404:
        print("더이상 페이지가 없습니다.")
        break
    
    page_num += 1


for line in total_craw.split("CVE"):
    if line == '\n':
        continue
    line = "CVE"+line
    list_value = []
    
    # 내부 구조
    for value in line.split('\n'):
        if value == '':
            continue
        list_value.append(value)
    total_info.append(list_value)

print(len(total_info))