from ludaweb import app
from flask import Flask, request, session, url_for, redirect, render_template, abort, g, flash, _app_ctx_stack, json
import requests
from ludaweb.models.models import db
from ludaweb.models.wxbind import Wxbind


@app.endpoint('widgets')
def widgets():
    app.logger.debug(request.json)
    app.logger.debug('code = ' + request.args.get('code'))
    url = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code' % (
        'wx68b01301d87f253a', '7c84b36db1cbe276c5a139c15a334494', request.args.get('code'))
    ret = requests.post(url, data={})
    openid = ret.json()['openid']
    menulist = [
        {'title': '企业基本信息', 'url': '#', 'color': 'bg-aqua', 'icon': 'fa-envelope-o'},
        {'title': '涉税事项查询', 'url': '#', 'color': 'bg-green', 'icon': 'fa-files-o'},
        {'title': '发票信息查询', 'url': '#', 'color': 'bg-yellow', 'icon': 'fa-flag-o'},
        {'title': 'A类纳税人信息查询', 'url': '#', 'color': 'bg-red', 'icon': 'fa-star-o'},
        {'title': '个人纳税信息查询', 'url': '#', 'color': 'bg-orange', 'icon': 'ion-ios-gear-outline'},
        {'title': '房产税缴纳情况查询', 'url': '#', 'color': ' bg-navy', 'icon': 'ion-ios-cloud-download-outline'}
    ]
    return render_template('menus.html', openid=openid, menus=menulist)


@app.endpoint('wxbind')
def wxbind():
    url = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&code=%s&grant_type=authorization_code' % (
        'wx68b01301d87f253a', '7c84b36db1cbe276c5a139c15a334494', request.args.get('code'))
    ret = requests.post(url, data={})
    openid = ret.json()['openid']
    return render_template('wxbind.html', openid=openid)


@app.endpoint('wxbindsave')
def wxbind_save():
    qysh = request.form['inputSh']
    openid = request.form['openid']
    qymc = request.form['inputQymc']
    xm = request.form['inputXm']
    sjhm = request.form['inputSjhm']

    url = 'http://www.tax.sh.gov.cn/jkfw/api/v1.0/services/sqhd/wxsfrz?qysh=%s&qymc=%s&sjhm=%s&xm=%s'
    ret = requests.get(url % (qysh, qymc, sjhm, xm))

    if ret.text == '1':

        temp_wxbind = None if Wxbind.query.filter_by(openid=openid) is None else Wxbind.query.filter_by(openid=openid).first()
        if temp_wxbind is not None:
            db.session.delete(temp_wxbind)

        wxbind = Wxbind(openid=openid, qysh=qysh)
        db.session.add(wxbind)
        try:
            db.session.commit()
            # app.logger.debug('db.session.commit()')
        except Exception as err:
            print(err)
            app.logger.error(err)
            db.session.rollback()
            return json.dumps(dict(result='fail', message='保存数据库异常'))
        return json.dumps(dict(result='success', message='微信绑定成功', qysh=qysh, qymc=qymc))
    else:
        return json.dumps(dict(result='fail', message='未通过实名制绑定校验'))
    return json.dumps(dict(result='success', message='微信绑定成功', qysh=qysh, qymc=qymc))


@app.endpoint('wxbindsuccess')
def wxbind_success():
    qysh = request.form['qysh']
    qymc = request.form['qymc']
    return render_template('wxbind_success.html', qysh=qysh, qymc=qymc)
