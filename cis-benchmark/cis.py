import json
import gspread
import time
import datetime


# service account key 파일 설정
sa_key_file = "[Key 파일]"
gc = gspread.service_account(sa_key_file)


# CIS Benchmark 실행 결과 파싱
with open("[실행 결과 파일]", "rt", encoding='UTF-8') as f:
    data = json.load(f)
    array = data["profiles"][0]["controls"]


# 스프레드시트 설정
sheet_url = "[결과 스프레드시트 url]"
sheet = gc.open_by_url(sheet_url)

now = datetime.datetime.now()
month = now.month
strMonth = str(month) + "월"
worksheet = sheet.worksheet(strMonth)


# ID(A열)와 결과(C열) 저장
num = []
status = []

for i in array:
    num.append(i["tags"]["cis_gcp"])
    status.append(i["results"][0]["status"])
    
    worksheet.batch_update(
        [
            {
                'range': 'A2',
                'values': [num],
                'majorDimension': 'COLUMNS'
            }
        ]
    )
    # gspread.exceptions.APIError: 'RATE_LIMIT_EXCEEDED' 방지를 위한 delay
    time.sleep(1.5)
    
    worksheet.batch_update(
        [
            {
                'range': 'C2',
                'values': [status],
                'majorDimension': 'COLUMNS'
            }
        ]
    )
    time.sleep(1.5)
