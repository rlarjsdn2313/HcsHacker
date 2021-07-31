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
      