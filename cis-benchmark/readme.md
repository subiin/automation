# **CIS Benchmark 결과 취합 자동화**

---
</br>


## 개요
- 목적
  * CIS Benchmark 결과를 시트에 수동으로 작성하던 불편함을 줄이고자 합니다.
  * 시트의 작성 과정을 자동화하여 MSP 월간보고서 작성 과정을 간소화하는 데에 목적이 있습니다.
- 파일 설명
  * CIS Benchmark를 수행하여 생성된 json 형태의 결과 파일을 파싱하여 항목 ID와 그 결과를 스프레드시트에 자동으로 업데이트합니다.
    * cis.py : 자동화를 수행하는 메인 파일
    * CreateSheets.gs : 월별 워크시트를 자동으로 생성하는 스크립트이며, 스프레드시트 템플릿 복사 시 스크립트가 따라오므로 별도로 복사 혹은 수정 필요 없음

</br>

---
</br>


## 사용 서비스
- CIS Benchmark (https://github.com/GoogleCloudPlatform/inspec-gcp-cis-benchmark)
- Google Spreadsheet
- GCP Service Account key 파일
  * Viewer 권한 필요
- Apps Script
  * 해당 월의 결과가 저장될 워크시트를 자동으로 생성
    * 2월에 "2월" 워크시트가 생성되는 스크립트 수행
    * 이후에 생성된 워크시트에 cis.py가 결과를 업데이트함
</br>

--- 
</br>




## Pre-requisites
- "pip3 install gspread"를 실행하여 스프레드시트에 write하기 위해 필요한 gspread 모듈을 설치합니다.
- 스프레드시트 템플릿 복사하여 각 고객사 드라이브 폴더에 사본을 생성합니다.
  * https://docs.google.com/spreadsheets/d/1k12bIQK9khmlXFF_0lljVtPBK6lshuicWAzB5ScxKeo
  * 자동화를 처음 수행하는 달이 1월이 아니면 첫 수행 이전 달의 워크시트를 "0월"의 형태로 생성합니다.
    * 자동화가 수행되는 시점의 이전 달의 시트를 복사하기 때문입니다.
- "Editor" 권한을 가진 GCP 서비스 계정을 생성하여 키 파일도 생성합니다.
- CIS Benchmark를 수행하여 결과 파일(json)을 로컬 PC에 다운로드합니다.
  * "https://github.com/GoogleCloudPlatform/inspec-gcp-cis-benchmark"을 기준으로 하며, 수행 방식(Ruby Gem 혹은 Docker)은 상관 없습니다.
  * html, csv가 아닌 json 파일이 생성되도록 합니다.
- 만약 스프레드시트에 업데이트할 열의 위치를 수정한다면 cis.py 내 worksheet.batch_update의 range를 변경합니다.
  * range는 업데이트할 셀의 처음 위치를 의미합니다. 예) A2 : A2열부터 column순으로 셀 업데이트

</br>

---
</br>




## 실행 방법

CIS Benchmark 수행 및 결과 취합 과정은 아래와 같습니다.

1. Cloud Shell에서 CIS Benchmark 수행
2. 수행 결과 파일을 로컬 PC에 다운로드
3. 각 고객사 결과 취합 스프레드시트에 항목별 수행 결과 작성
4. 고객사에 스프레드시트 전송

해당 작업은 위의 3번 과정을 자동화하며, 추후 자동화의 범위를 확대할 예정입니다.

- 스프레드시트에 업데이트되는 열은 (json 결과 파일 key 기준)cis_gcp와 status입니다.
  * cis_gcp : data["profiles"][0]["controls"]["tags"]["cis_gcp"]
  * status : data["profiles"][0]["controls"]["results"][0]["status"]
   

실행 방법은 다음과 같습니다.

1. 서비스 계정 키파일과 CIS Benchmark 수행 결과 파일의 경로를 cis.py에 입력합니다.
2. 사본 생성한 결과 스프레드시트 url을 cis.py에 입력합니다.
  * 사본 생성은 Apps Script의 트리거 기능으로 매월 자동 생성됩니다.
3. 



</br>

---
</br>


## 주의 및 제약 사항
- cis.py에 수정사항이 생겨 업데이트를 할 경우 Source Repositories에 서비스 계정 키 파일이 업로드되지 않도록 주의합니다.
- 스프레드시트 템플릿의 B열(보안정책)이 고객사의 CIS Benchmark 수행 결과의 수행 항목과 일치하는지 확인합니다.
  * CIS Benchmark의 수행 항목이 업데이트될 경우 스프레드시트와 불일치하게 됩니다.
- gspread.exceptions.APIError: 'RATE_LIMIT_EXCEEDED' 에러가 발생하지 않도록 sleep 함수를 유지해야 합니다.
  * 1 User 당 1분에 스프레드시트에 write할 수 있는 개수는 60개이므로, 에러가 발생하지 않는 선에서 delay를 조정 가능합니다.

</br>

---
</br>

