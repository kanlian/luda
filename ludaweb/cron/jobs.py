# -*- coding: utf-8 -*-
import apscheduler
import requests
from flask import g, json
from flask import jsonify

from ludaweb import app, get_client, Wxbind


def query_wechat_answer(a, b):
    app.logger.error("======================= 进入定时任务 =======================")
    with app.app_context():
        # 获取微信客户端对象
        wxclient = get_client()
        # 远程接收消息URL
        url = 'http://www.tax.sh.gov.cn/jkfw/api/v1.0/services/sqhd/receivemsg'
        ret = requests.get(url)
        data = json.loads(ret.text)
        app.logger.debug('=======================' + ret.text)
        if data['retcode'] == '1':  # 获取成功
            l = list(map(lambda x: {'hfnr': x['hfnr'], 'fssj': x['fssj'],
                                    'openid': ('' if Wxbind.query.filter_by(
                                        qysh=x['qysh']) is None else Wxbind.query.filter_by(
                                        qysh=x['qysh']).first().openid)}, data['xxlist']))
            # 发送微信
            for xx in l:
                try:
                    wxclient.send_text_message(xx['openid'], xx['hfnr'])
                except Exception as ex:
                    app.logger.error('=======================发送微信失败,', ex)
        else:
            app.logger.debug('=======================retcode != 1 ' + ret.text)

    app.logger.error('======================= 结束定时任务 =======================')
