# ltcnScCode, schulCrseScCode 분석을 위한 모듈
from hcskr.mapping import schoolinfo
import requests


# API 요청을 할 URL
api_url = 'https://hcs.eduro.go.kr/v2/searchSchool'

# API에 전달해야 하는 값들
'''
Request
1. ltcnScCode: 지역코드
2. schulCrseScCode: 학교급
3. orgName: 학교 이름
4. loginType: 로그인 형태(기본값: school)
'''


def search_school(area, school_name, school_level):
      # 지역, 학교급 분석하여 얻은 지역코드와 학교급 코드를 info 변수에 저장
      info = schoolinfo(area, school_level)

      # API에 전달할 정보들을 data 변수에 저장
      data = {
            'ltcnScCode': info['schoolcode'],
            'schulCrseScCode': info['schoollevel'],
            'orgName': school_name,
            'loginType': 'school'
      }

      # request.get 함수를 사용해 API에 학교 검색 요청, API로부터 전달받은 값을 res 변수에 저장
      res = requests.get(
            api_url,
            data
      ).json()

      # API에서 얻은 값을 출력
      print(res)


'''
예시 입력
search_school('서울', '장승중', '중')

예시 출력
{
      'schulList': [
            {
                  'orgCode': 'B100001573', 
                  'kraOrgNm': '장승중학교', 
                  'engOrgNm': 'Jangseung Middle School', 
                  'insttClsfCode': '5', 
                  'lctnScCode': '01', 
                  'lctnScNm': '서울특별시', 
                  'sigCode': '11590', 
                  'juOrgCode': 'B100000304', 
                  'schulKndScCode': '03', 
                  'orgAbrvNm01': '장승중학교', 
                  'orgAbrvNm02': '장승중학교', 
                  'orgUon': 'Y', 
                  'updid': 'SYSTEM', 
                  'mdfcDtm': '2020-08-19 19:48:48.0', 
                  'atptOfcdcConctUrl': 'senhcs.eduro.go.kr', 
                  'addres': '(06963)서울특별시 동작구 장승배기로10가길 25 , 장승중학교 (상도동)'
            }, 
            {
                  'orgCode': 'J100005791', 
                  'kraOrgNm': '장승중학교(개교예정)', 
                  'engOrgNm': '장승중학교(개교예정)', 
                  'insttClsfCode': '5', 
                  'lctnScCode': '10', 
                  'lctnScNm': '경기도', 
                  'sigCode': '41360', 
                  'juOrgCode': 'J100000170', 
                  'schulKndScCode': '03', 
                  'orgAbrvNm01': '장승중학교(개교예정)', 
                  'orgAbrvNm02': '장승중학교(개교예정)', 
                  'orgUon': 'Y', 
                  'updid': 'SYSTEM', 
                  'mdfcDtm': '2020-08-19 20:17:42.0', 
                  'atptOfcdcConctUrl': 'goehcs.eduro.go.kr', 
                  'addres': '(472864)경기도 남양주시 진접읍 부평로48번길 35-40 (진접읍)'
            }
      ], 
      'sizeover': False
}
'''
