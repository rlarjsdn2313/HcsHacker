import requests


api_url = 'https://hcs.eduro.go.kr/v2/searchSchool'

def generate_url(school_url, end_point):
      return f'https://{school_url}hcs.eduro.go.kr{end_point}'


def search_school(area, school_name, school_level):
      info = schoolinfo(area, school_level)

      data = {
            'ltcnScCode': info['schoolcode'],
            'schulCrseScCode': info['schoollevel'],
            'orgName': school_name,
            'loginType': 'school'
      }

      res = requests.get(
            generate_url('', '/v2/searchSchool'),
            data
      ).json()

      return {
            'res': res,
            'info': info
      }