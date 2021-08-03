# 학교 검색을 위한 모듈
from search_school import search_school
# 자가진단 API에서 원하는 키로 암호화하기 위한 모듈
from hcskr.mapping import encrypt
# API에 요청을 보내기 위한 모듈
import requests


# 교육청 도메인
domain = 'sen'
# API 요청을 할 URL
api_url = f'https://{domain}hcs.eduro.go.kr/v2/findUser'
# domain이 'sen'일 때 api_url은 'https://senhcs.eduro.go.kr/v2/findUser'이 됨

# API에 전달해야 하는 값들
'''
Request
1. birthday: 암호화된 생일(YYMMDD)
2. loginType: 로그인 형태(기본값: school)
3. name: 암호화된 이름
4. orgCode: 학교 코드(학교 검색 API에서 얻음)
5. stdntPNo: 학생 번호(기본값: None)
'''


def login(area, school_name, school_level, birthday, name):
      # 학교 검색 API를 통해 학교에 대한 정보를 가지고 와 school_data 변수에 저장
      school_data = search_school(area, school_name, school_level)
      # school_data에 검색된 학교들 중 가장 첫번째로 검색된 학교의 학교 코드를 org_code에 저장
      org_code = school_data['schulList'][0]['orgCode']

      # API에 전달할 정보들을 data 변수에 저장
      data = {
            'birthday': encrypt(birthday),
            'loginType': 'school',
            'name': encrypt(name),
            'orgCode': org_code
      }

      # request.post 함수를 사용해 POST 형식으로 API에 학생 로그인 요청, API로 부터 전달받은 값을 dict 형태로 res에 저장
      res = requests.post(
            api_url,
            json=data
      ).json()

      # API에서 얻은 값을 리턴
      return res


'''
예시 입력
print(login('서울', '장승중', '중', '070208', '김건우'))

예시 출력
{
      'orgName': '장승중학교', 
      'admnYn': 'N', 
      'atptOfcdcConctUrl': 'senhcs.eduro.go.kr', 
      'mngrClassYn': 'N', 
      'pInfAgrmYn': 'Y', 
      'userName': '김건우', 
      'stdntYn': 'Y', 
      'token': 'Bearer 0156DA8A6E9048A8E2F89EA13121C4D57F0275772748E63C1D7B6B0B1C1C721DB4BC351C49BE11B5A454EEC72EAF7F9595225F924590A8DB6C001DD517602259D57FD2BBB2350DDB2F9CA00DCBB13E2DD6E6A7F406AFA3BCF7924B76D33AC9901AF75072175612A981222B132637F60CD4DDA474E9763F1B2A2BEF89E38DFEE468C09BF6A8DA8AF92F129FCF6F5D0587FCD3DA', 
      'mngrDeptYn': 'N'
}
'''
