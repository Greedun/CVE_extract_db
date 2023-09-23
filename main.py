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
#sys.exit()

# 2. cve에 나온 내용 크롤링
print(f"[*] CVE 크롤링 start - {input_vendor}")
total_info = [] # [cve_name, vendors ,products ,update_date ,cvss_v2 ,cvss_v3 ,desc_en]

page_num = 1
total_craw = ''
while True:
    
    page_path = target_path + str(page_num)
    response = requests.get(page_path)
    #print(target_path)
    
    print(f"    => page {page_num} 진행중")
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
print(f"[*] CVE 크롤링 finish")

print(f"[*] 크롤링된 데이터 가공중")
list_craw = total_craw.split(".\nCVE")
list_craw[0] = list_craw[0][4:]

for line in list_craw:
    line = "CVE" + line
    
    list_line = line.split('\n')
    # [cve_name, vendors ,products ,update_date ,cvss_v2 ,cvss_v3 ,desc_en]
    list_line = list(filter(None, list_line)) # 7개
    
    total_info.append(list_line)
print(f"[*] 가공 완료")

print(f"[*] insert data")
# total_info에 담긴 데이터를 splite에 insert
con = sqlite3.connect('cve_extract.db')
cur = con.cursor()
for row in total_info:
    if len(row) == 1:
        print(row)
        sys.exit()
    cur.execute("""INSERT INTO cve_extract 
                (cve_name, vendors ,products ,update_date ,cvss_v2 ,cvss_v3 ,desc_en)
                VALUES (?, ?, ?, ?, ?, ?, ?)"""
                ,(row[0], row[1], row[2], row[3], row[4], row[5], row[6])
                )
con.commit()
con.close()