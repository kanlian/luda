import re

import requests
from requests.adapters import HTTPAdapter


class Tuling(object):
    """
    深度整合的图灵机器人
      """
    'API 文档: http://doc.tuling123.com/openapi2/263611'

    url = 'http://openapi.tuling123.com/openapi/api/v2'

    def __init__(self, api_key=None, user_id=None):
        """
        :param api_key: 你申请的 api key
        """
        self.session = requests.Session()
        for p in 'http', 'https':
            self.session.mount(
                '{}://'.format(p),
                HTTPAdapter(
                    pool_connections=10,
                    pool_maxsize=10,
                    max_retries=3,
                ))

        self.api_key = api_key or 'e4701768941a4323be76fa24d5e251a1'
        self.user_id = user_id or '123456'

    def get_answer(self, msg, user_id):
        def process_answer():
            ret = str()

            items = answer.get('results', list())
            for item in items:
                resulttype = item.get('resultType')
                if resulttype == 'text':
                    ret += item.get('values').get('text')
                elif resulttype == 'news':
                    news = item.get('values').get('news')
                    for new in news:
                        ret += '\n\n{}\n{}'.format(
                            new.get('info') or new.get('name'),
                            new.get('detailurl')
                        )
                elif resulttype == 'url':
                    ret += '\n{}'.format(item.get('values').get('url'))
            return ret

        user_id = re.sub(r'[^a-zA-Z\d]', '', user_id)
        user_id = user_id[-32:]
        user_id = 123456
        ###
        # user_id为int类型
        ###
        payload = dict(
            perception=dict(inputText=dict(text=msg)),
            userInfo=dict(apiKey=self.api_key, userId=user_id)
        )
        try:
            r = self.session.post(self.url, json=payload)

            answer = r.json()
        except Exception as err:
            print(err)
            answer = None
        finally:
            return process_answer()
