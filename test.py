import sqlite3

# SQLite 데이터베이스 파일 생성 또는 연결
conn = sqlite3.connect('my_database.db')

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
