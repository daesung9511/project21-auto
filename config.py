# 정산시트 파일 경로
KEY_SHEET_FILE_PATH = ""

# ex) MAC "/Users/qualson/Library/Application Support/Google/Chrome"
CHROME_USER_DATA_PATH = "C:\\Users\\krims\\AppData\\Local\\Google\\Chrome\\User Data"

# ex) "Profile 2"
CHROME_PROFILE_NAME = "Profile 2"

CHROME_GFA_PROFILE_NAME = "Profile 3"

# 파일들 저장 경로
RAW_FILE_PATH = "rd_file"

GOOGLE_ADS_PATH = "C:\\Users\\krims\\eclipse-workspace\\project21-auto\\googleads.yaml"

# 매칭테이블 포함 데이터 엑셀 파일
RD_FILE = {
    "lavena": "lavena_rd_data.xlsx",
    "anua": "anua_rd_data.xlsx",
    "yuge": "yuge_rd_data.xlsx",
    "project21": "project21_rd_data.xlsx",
}

# 브랜드별 구분값 설정 
CUTOFF_VERSION = {
    "lavena" : "201208",
    "anua": "201208",
    "yuge": "201208",
    "project21": "201208",
}

# 예외 판매처 키워드 설정
# 해당 키워드가 들어있는 판매처명은 RD에서 제외됩니다. 
EXCLUDE_KEYWORD = {
    "lavena" : [],
    "anua": [ "쇼피", "큐텐", "수출" ],
    "yuge": [],
    "project21": [],
}
