import requests

url = 'http://openapi.tuling123.com/openapi/api/v2'

param1 = dict(
    perception=dict(inputText=dict(text='上海天气')),
    userInfo=dict(apiKey='e4701768941a4323be76fa24d5e251a1',userId='123456')
)

param = {
    "perception": {
        "inputText": {
            "text": "附近的酒店"
        },
        "selfInfo": {
            "location": {
                "city": "北京",
                "latitude": "39.45492",
                "longitude": "119.239293",
                "nearest_poi_name": "上地环岛南",
                "province": "北京",
                "street": "信息路"
            },
        }
    },
    "userInfo": {
        "apiKey": "e4701768941a4323be76fa24d5e251a1",
        "userId": "123456"
    }
}

ret = requests.post(url, json=param1)

print(ret.content)
