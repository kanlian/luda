# -*- coding: utf-8 -*-
import requests

from ludaweb.api.apps import App
from werobot.contrib.flask import make_view
from werobot.client import Client
from werobot.config import Config
from werobot.parser import parse_user_msg

from ludaweb.models.wxbind import Wxbind
from ludaweb.tuling_bot.tulingbot import Tuling

__version__ = '0.1'
from flask import Flask, g
from flask_restful import Api, Resource
from celery import Celery

app = Flask('ludaWeb')
app.debug = True

# app.config['CELERY_BROKER_URL'] = 'redis://47.92.37.219:6379/0'
# app.config['CELERY_RESULT_BACKEND'] = 'redis://47.92.37.219:6379/0'
#
# celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
# celery.conf.update(app.config)

# import controllers
from ludaweb.controllers import *

# import model
from ludaweb.models.models import db

#### initial logger ####
import logging
from logging.handlers import RotatingFileHandler
import os

LOG_PATH = '/'.join((os.path.dirname(os.path.realpath(__file__)), 'log'))
if not os.path.exists(LOG_PATH):
    os.makedirs(LOG_PATH)

handler = RotatingFileHandler(LOG_PATH + '/debug.log', maxBytes=10000, backupCount=1)
handler.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)
#### initial logger ####


#### initial sesion ####
from datetime import timedelta

app.config['SECRET_KEY'] = 'random'
app.permanent_session_lifetime = timedelta(seconds=60 * 60 * 10)  # session expire time
#### initial sesion ####


#### initial database ####
APP_ROOT = os.path.dirname(os.path.realpath(__file__))

app.config.from_pyfile(os.path.join(APP_ROOT, 'config') + '/database.cfg')
db.init_app(app)
#### initial database ####

app.debug = False

#### router ####
from werkzeug.routing import Rule

urlpatterns = [
    Rule('/', endpoint='index'),
    Rule('/widgets', endpoint='widgets'),
    Rule('/wxbind', endpoint='wxbind'),
    Rule('/wxbind/save', endpoint='wxbindsave'),
    Rule('/applications', endpoint='applications'),
    Rule('/applications/add', endpoint='addapplications'),
    Rule('/applications/save', endpoint='saveapplications'),
    Rule('/qstb/<int:id>', endpoint='qstb'),
    Rule('/mps/webhook', endpoint='webhook', methods=['GET', 'POST']),
    Rule('/ics', endpoint='ics'),
]
api = Api(app)
api.add_resource(App, '/api/applications')

for rule in urlpatterns:
    app.url_map.add(rule)

#### router ####

#### wechat ####
import werobot

robot = werobot.WeRoBot(token='69b3f633cd9e4136bfdd8be812a34e28')

config = Config()
basedir = os.path.dirname(os.path.abspath(__file__))
config.from_pyfile(os.path.join(basedir, "client_config.py"))
client = Client(config=config)

from werkzeug.local import LocalProxy


def get_client():
    return client


tulingbot = Tuling()
###client.get_menu
'''
client.create_menu({
    "button": [
        {
            "name": "办事指南",
            "sub_button": [
                {
                    "type": "click",
                    "name": "最新政策",
                    "key": "zxzc"
                }, {
                    "type": "click",
                    "name": "最新通知",
                    "key": "zxtz"
                }, {
                    "type": "click",
                    "name": "征期日历",
                    "key": "zqrl"
                }, {
                    "type": "click",
                    "name": "热点扫描",
                    "key": "rdsm"
                }, {
                    "type": "click",
                    "name": "办税地图",
                    "key": "bsdt"
                }]
        },
        {

            "name": "便民办税",
            "sub_button": [
                {
                    "type": "view",
                    "name": "我要查询",
                    "url": "https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx68b01301d87f253a&redirect_uri=http://www.yeyepaodecha.com/widgets&response_type=code&scope=snsapi_base&state=1#wechat_redirect"

                }, {
                    "type": "click",
                    "name": "纳税人学堂",
                    "key": "nsrxt"
                }, {
                    "type": "click",
                    "name": "自助办税服务终端",
                    "key": "zzbsfwzd"
                }, {
                    "type": "click",
                    "name": "网上办税服务厅",
                    "key": "wsbsfwt"
                }, {
                    "type": "click",
                    "name": "十二万申报",
                    "key": "srwsb"
                }]
        },
        {
            "name": "特色服务",
            "sub_button": [
                {
                    "type": "view",
                    "name": "微网厅",
                    "url": "http://www.tax.sh.gov.cn/wtwx/home/init.do"
                },
                {
                    "type": "click",
                    "name": "授权获取",
                    "key": "GET_QX"
                },
                {
                    "type": "view",
                    "name": "微信绑定",
                    "url": "https://open.weixin.qq.com/connect/oauth2/authorize?appid=wx68b01301d87f253a&redirect_uri=http://www.yeyepaodecha.com/wxbind&response_type=code&scope=snsapi_base&state=1#wechat_redirect"
                }
            ]
        }
    ]})

'''


@robot.click
def abort(message):
    if message.key == "V1001_TODAY_MUSIC":
        return "I'm a robot"
    elif message.key == "GET_QX":
        return message.source
    else:
        return message.key


@robot.view
def vi(message):
    if message.key == "V1001_TODAY_MUSIC":
        return "I'm a robot"
    elif message.key == "GET_QX":
        return message.source


@robot.text
def echo(message):
    app.logger.error(message.source)
    # ret = tulingbot.get_answer(message.content, message.source)
    # app.logger.error(ret)
    wxbind = Wxbind.query.filter_by(openid=message.source)
    if wxbind is not None:
        wxbind = wxbind.first()

    url = 'http://www.tax.sh.gov.cn/jkfw/api/v1.0/services/sqhd/sendmsg?qysh=%s&nr=%s' % (wxbind.qysh, message.content)
    requests.get(url, data={})
    # return ret


app.add_url_rule(rule='/robot/',  # WeRoBot 挂载地址
                 endpoint='werobot',  # Flask 的 endpoint
                 view_func=make_view(robot),
                 methods=['GET', 'POST'])
#### wechat ####

### 定时任务
from flask_apscheduler import APScheduler


class Config(object):
    JOBS = [
        {
            'id': 'job1',
            'func': 'cron.jobs:query_wechat_answer',
            'args': (1, 2),
            'trigger': 'interval',
            'seconds': 60
        }
    ]


app.config.from_object(Config())
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()
##  定时任务
