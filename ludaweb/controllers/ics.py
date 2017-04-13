import re
from uuid import uuid1

from flask import make_response
from icalendar import Calendar, Event
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from ludaweb import app


def display(cal):
    return cal.to_ical().decode('utf-8').replace('\r\n', '\n').strip()


def get_ics(schedule):
    cal = Calendar()
    cal['version'] = '2.0'
    cal['prodid'] = '-//CQUT//Syllabus//CN'  # *mandatory elements* where the prodid can be changed, see RFC 5445
    start_monday = date(2017, 2, 20)  # 开学第一周星期一的时间 TODO: 从 http://cale.dc.cqut.edu.cn/Index.aspx?term=2016-2017 抓取开学时间
    dict_week = {'一': 0, '二': 1, '三': 2, '四': 3, '五': 4, '六': 5, '日': 6}
    dict_day = {1: relativedelta(hours=8, minutes=20), 3: relativedelta(hours=10, minutes=20),
                5: relativedelta(hours=14, minutes=0), 7: relativedelta(hours=16, minutes=0),
                9: relativedelta(hours=19, minutes=0)}
    for line in schedule:
        event = Event()
        print(line)
        # line should be like this: ['汇编语言程序设计', '周三第7,8节', '第10-10周|双周', '第1实验楼B403-A', '刘小洋(刘小洋)']

        info_day = re.findall(r'周(.*?)第(\d+),(\d+)节', line[1], re.S | re.M)
        info_day = info_day[0]
        print(info_day)
        # info_day should be like this: ('三', '7', '8')

        info_week = re.findall(r'第(\d+)-(\d+)周', line[2], re.S | re.M)
        info_week = info_week[0]
        print(info_week)
        # info_week should be like this: ('10', '10')

        dtstart_date = start_monday + relativedelta(weeks=(int(info_week[0]) - 1)) + relativedelta(
            days=int(dict_week[info_day[0]]))
        dtstart_datetime = datetime.combine(dtstart_date, datetime.min.time())
        dtstart = dtstart_datetime + dict_day[int(info_day[1])]
        dtend = dtstart + relativedelta(hours=1, minutes=40)
        # 我们的课持续一小时四十分钟（中间有十分钟课间时间）
        if int(info_day[1]) == 9:
            dtend = dtend - relativedelta(minutes=5)
        # 我们晚上的课要少五分钟课间时间

        event.add('uid', str(uuid1()) + '@CQUT')
        event.add('summary', line[0])
        event.add('dtstamp', datetime.now())
        event.add('dtstart', dtstart)
        event.add('dtend', dtend)

        if line[2].find('|') == -1:
            interval = 1
            count = int(info_week[1]) - int(info_week[0]) + 1
        else:
            interval = 2
            count = int(info_week[1]) - int(info_week[0]) / 2 + 1
        # 如果有单双周的课 那么这些课隔一周上一次

        event.add('rrule',
                  {'freq': 'weekly', 'interval': interval,
                   'count': count})
        # 设定重复次数

        event.add('location', line[3])
        # 设定重复地点

        cal.add_component(event)
    return cal


@app.endpoint('ics')
def index():
    app.logger.info("请求日历服务...")
    schedule = [['税务培训', '周一第1,2节', '第1-10周', '建国中路29号5楼', '韦建卫'],
                ['发票购买', '周二第1,2节', '第1-10周', '建国中路29号5楼', '周敏'],
                ['资源税', '周三第1,2节', '第4-18周|双周', '建国中路29号5楼', '杜云飞'],
                ['流转税、企业税得税、个人所得税', '周五第1,2节', '第1-10周', '建国中路29号5楼', '周敏'],
                ['房产税（企业）', '周一第3,4节', '第1-10周', '建国中路29号5楼', '柯芳'],
                ['城镇土地使用税（按季申报、按半年申报）', '周二第3,4节', '第8-10周', '建国中路29号5楼', '刘小洋(刘小洋)'],
                ['城镇土地使用税（按季申报、按半年申报） ', '周二第3,4节', '第12-16周', '建国中路29号5楼', '刘小洋(刘小洋)'],
                ['申报缴纳工会经费税务代收', '周三第3,4节', '第1-10周', '建国中路29号5楼', '韦建卫'],
                ['2016年度企业所得税汇算清缴', '周四第3,4节', '第13-18周', '建国中路29号5楼', '杜云飞'],
                ['申报缴纳2017年度车船税', '周四第3,4节', '第2-10周', '建国中路29号5楼', '杜云飞'],
                ['申报缴纳资源税、按期汇总缴纳纳税人和电子应税凭证纳税人申报缴纳印花税', '周五第3,4节', '第1-4周', '建国中路29号5楼', '韦建卫'],
                ['申报缴纳增值税、消费税、城市维护建设税、教育费附加、地方教育附加、文化事业建设费、个人所得税、企业所得税、核定征收印花税、申报缴纳残疾人就业保障金', '周二第5,6节', '第12-13周', '建国中路29号5楼', '唐朝君'],
                ['申报缴纳2017年度车船税', '周二第5,6节', '第1-10周', '建国中路29号5楼', '唐朝君'],
                ['按季度申报缴纳的土地增值税预缴税款', '周三第5,6节', '第8-10周', '建国中路29号5楼', '刘小洋(刘小洋)'],
                ['按季度申报缴纳的土地增值税预缴税款', '周三第5,6节', '第12-16周', '建国中路29号5楼', '刘小洋(刘小洋)'],
                ['工会经费税务代收', '周三第5,6节', '第1-5周', '建国中路29号5楼', '柯芳'],
                ['特定行业个人所得税年度申报', '周四第5,6节', '第1-17周', '建国中路29号5楼', '胡洪波'],
                ['企事业单位承包承租经营者个人所得税年度纳税申报', '周五第5,6节', '第1-1周|单周', '建国中路29号5楼', '唐朝君'],
                ['2016年“年所得12万元以上”纳税人自行纳税申报', '周五第5,6节', '第12-13周', '建国中路29号5楼', '唐朝君'],
                ['分次取得承包、承租经营所得个人所得税年度汇算清缴', '周五第5,6节', '第3-10周', '建国中路29号5楼', '唐朝君'],
                ['个人独资企业投资者和合伙企业合伙人、企事业单位承包承租经营者在中国境内两处或者两处以上取得所得的个人所得税年度汇总纳税申报', '周二第7,8节', '第10-10周|双周', '建国中路29号5楼-A', '刘小洋(刘小洋)'],
                ['特定行业个人所得税年度申报', '周二第7,8节', '第12-16周', '建国中路29号5楼-A', '刘小洋(刘小洋)'],
                ['2016年度企业所得税汇算清缴', '周三第7,8节', '第10-10周|双周', '建国中路29号5楼-A', '刘小洋(刘小洋)'],
                ['地税无应纳税（费）款申报', '周三第7,8节', '第12-16周', '建国中路29号5楼-A', '刘小洋(刘小洋)'],
                ['从中国境外取得所得的纳税义务人申报缴纳个人所得税', '周二第9,10节', '第9-9周|单周', '建国中路29号5楼', '张伶俐'],
                ['2017年“年所得12万元以上”纳税人自行纳税申报', '周二第9,10节', '第6-8周', '建国中路29号5楼', '张伶俐'],
                ['分次取得承包、承租经营所得个人所得税年度汇算清缴', '周二第9,10节', '第1-4周', '建国中路29号5楼', '张伶俐'],
                ['按季度申报缴纳的土地增值税预缴税款', '周四第9,10节', '第1-8周', '建国中路29号5楼', '张伶俐']]
    for line in schedule:
        print(line)
    print("\n正在生成 ics 文件...")
    ics = get_ics(schedule)
    print(display(ics))
    print("生成成功!")
    response = make_response(display(ics))
    response.content_type = 'application/text'
    return response

