# 로그인을 위한 모듈
from attr.setters import validate
from login import login
# 비밀번호 암호화를 위해 필요한 모듈
from hcskr.transkey import mTransKey
# API에 요청을 보내기 위한 모듈
import requests
# 비동기 처리를 위해 필요한 모듈
import asyncio
# json data 처리를 위한 모듈
import json


# API 요청을 할 URL을 api_url에 저장
domain = 'sen'
api_url = f'https://{domain}hcs.eduro.go.kr/v2/validatePassword'

'''
Request
1. deviceUuid: 기기 고유값(기본값: '')
2. makeSession: ?(기본값: True)
3. password: 암호화된 비밀번호
'''


# 비밀번호 암호화 함수 -> asyncio.get_event_loop().run_until_complete(encrypt_password('2313'))
async def encrypt_password(password):
      mtk = mTransKey('https://hcs.eduro.go.kr/transkeyServlet')
      pw_pad = await mtk.new_keypad(
            'number', 'password', 'password','password'
      )
      encrypted = pw_pad.encrypt_password(password)
      hm = mtk.hmac_digest(encrypted.encode())


      data = {
                  "password": json.dumps(
                        {
                              "raon": [
                              {
                                    "id": "password",
                                    "enc": encrypted,
                                    "hmac": hm,
                                    "keyboardType": "number",
                                    "keyIndex": mtk.keyIndex,
                                    "fieldType": "password",
                                    "seedKey": mtk.crypto.get_encrypted_key(),
                                    "initTime": mtk.initTime,
                                    "ExE2E": "false",
                              }
                              ]
                        }
                  ),
                  "deviceUuid": "",
                  "makeSession": True,
      }


      # 암호화된 비밀번호가 들어있는 data를 리턴
      return data


def validate_password(name, birth, area, school_name, school_level, password):
      # 학생 인증 토큰을 token에 저장
      token = login(
            area, school_name, school_level, birth, name
      )['token']

      # API에 전송할 headers
      headers = {
            "Referer": "https://hcs.eduro.go.kr/",
            "Authorization": token,
            "X-Requested-With": "XMLHttpRequest",
            "Content-Type": "application/json;charset=utf-8",
      }

      # data 준비
      data = asyncio.get_event_loop().run_until_complete(encrypt_password(password))

      res = requests.post(
            api_url, headers=headers, json=data
      ).json()

      return res


'''
예시 입력
print(validate_password(
      '김건우', '070208', '서울', '장승중', '중', 비밀번호
))

예시 출력
1. 비밀번호가 틀렸을 때
{
      'isError': True,
      'statusCode': 252,
      'errorCode': 1001,
      'data': {
            'failCnt': 틀린 횟수,
            'canInitPassword': False
      }
}

2. 비밀번호가 맞았을 때
사용자의 인증 토큰이 리턴됨

3. 비밀번호가 5회 이상 틀렸을 때
{
      'isError': True,
      'statusCode': 252,
      'errorCode': 1000,
      'data': {'remainMinutes': 남은 시간}
}
'''
