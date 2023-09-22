# library
import sqlite3
from sqlite3 import Error
import sys

input_vendor = input("CVE를 추출하고 싶은 vendor를 고르시오")
db_name = "CVE_extract.db"
table_name = "CVE_extract"

base_path = "https://www.opencve.io/cve?vendor=" # + {input_vendor}
target_path = base_path+input_vendor

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
create_db()

# 2. 






