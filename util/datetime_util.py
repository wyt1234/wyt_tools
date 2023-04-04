from datetime import datetime, timedelta


# 当天早上九点(08:55)
def oneday_moring(d=datetime.now()):
    d = d.strftime("%Y-%m-%d") + "08:55"
    d = datetime.strptime(d, '%Y-%m-%d%H:%M')
    return d


# 第二天早上
def next_moring(d=datetime.now()):
    date_after = d + timedelta(days=1)
    return oneday_moring(date_after)


# 下周一
def next_monday(d=datetime.now(), weekday=1):
    """获取下周几日期
      :param weekday: weekday取值1-7
      :param d: 原日期，默认当前时间
      :return: datetime.datetime
      """
    delta = weekday - d.isoweekday()
    if delta <= 0:
        delta += 7
    return oneday_moring(d + timedelta(days=delta))


# 下个月第一个周一
def next_first_monday(d=datetime.now()):
    # 获取下一个月的第一天
    '''
    param: month_str 月份，2021-04
    '''
    # return: 格式 %Y-%m-%d
    month_str = d.strftime('%Y-%m')
    year, month = int(month_str.split('-')[0]), int(month_str.split('-')[1])
    if month == 12:
        year += 1
        month = 1
    else:
        month += 1
    next_month_first_day = '{}-{}-01'.format(year, month)
    d = next_month_first_day
    d = datetime.strptime(d, '%Y-%m-%d')
    for i in range(30):
        t = d + timedelta(days=i)
        if t.isoweekday() == 1:
            return oneday_moring(t)
    print('计算下个月第一个周一异常')
    return d


if __name__ == '__main__':
    d = datetime.now()
    print(next_moring(d))
    print(next_monday(d))
    print(next_first_monday(d))
    print(f'修改前日期：{d}')
