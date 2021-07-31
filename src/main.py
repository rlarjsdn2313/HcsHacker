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
# password = '2313'
# info = {}


# def generate_url(school_url, end_point):
#       return f'https://{school_url}hcs.eduro.go.kr{end_point}'


# def search_school(area, school_name, school_level):
#       info = schoolinfo(area, school_level)

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


name = str(input('Name: '))
birth = str(input('Birth: '))
area = str(input('Area: '))
school_name = str(input('School Name: '))
school_level = str(input('School Level: '))
test_password = str(input('Test Password: '))

count = 1


while True:
      for _ in range(6):
            hcskr.generatetoken(name, birth, area, school_name, school_level, test_password)
      
      print(f'\rBlock {count} time', end='')
      count += 1

      time.sleep(5 * 60 + 0.5)