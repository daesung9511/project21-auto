# 정산시트 파일 경로
KEY_SHEET_FILE_PATH = ""

# ex) MAC "/Users/qualson/Library/Application Support/Google/Chrome"
CHROME_USER_DATA_PATH = "C:\\Users\\i02\\AppData\\Local\\Google\\Chrome\\User Data"

# ex) "Profile 2"
CHROME_PROFILE_NAME = "Profile 2"

CHROME_GFA_PROFILE_NAME = "Profile 2"

# 파일들 저장 경로
# RAW_FILE_PATH = "C:\\Users\\i02\\주식회사더파운더즈\\이선형 - 더파운더즈(전체) (1)\\13_오퍼레이션\\01_판매실적"
RAW_FILE_PATH = "C:\\Users\\i02\\OneDrive - 주식회사더파운더즈 (2)\\01_판매실적"

GOOGLE_ADS_PATH = "C:\\Users\\i02\\project21-auto\\googleads.yaml"

# 매칭테이블 포함 데이터 엑셀 파일
RD_FILE = {
    "lavena": "02.라베나_이지어드민_데이터 정리_2020 ★.xlsx",
    "anua": "02.아누아_이지어드민_데이터 정리_헤더변경 ★.xlsx",
    "yuge": "02.유즈_이지어드민_데이터 정리_헤더변경 ★.xlsx",
    "project21": "02.프로젝트21_이지어드민_데이터 정리_실데이터_헤더변경 ★.xlsx",
}
# 브랜드별 구분값 설정 
CUTOFF_VERSION = {
    "lavena" : "220107",
    "anua": "211228",
    "yuge": "211228",
    "project21": "210802",
}

# 예외 판매처 키워드 설정
# 해당 키워드가 들어있는 판매처명은 RD에서 제외됩니다. 
EXCLUDE_KEYWORD = {
    "lavena" : [],
    "anua": [ "쇼피", "큐텐", "수출", "해외", "시코르", "라자다" ],
    "yuge": [],
    "project21": [],
}
