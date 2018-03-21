from datetime import datetime
from datetime import timedelta


def str2list(x):
    #use this method when eval of list does not fit in memory
    aux = x[1:-1]
    aux = aux.split(', ')
    aux = [eval(_) for _ in aux]
    return aux


def save_data(filepath, data, kind='w'):
    fw = open(filepath, kind)
    fw.write(data)
    fw.close()


def date2days(value):
    base = datetime(2017, 1, 1, 0, 0)
    value = datetime.strptime(str(value), '%Y%m%d')
    delta = value-base
    return delta.days


def days2date(delta):
    base = datetime(2017, 1, 1, 0, 0)
    date = base + timedelta(int(delta))
    value = date.strftime('%Y%m%d')
    return int(value)


def traintest(what, n): 
    #by default, we will predict last 5 elements
    assert n > 0, 'traintest error 1'
    assert n < 7, 'traintest error 2'
    ret = []
    for i in range(-5,0):
        train = what[i-n:i]
        test = [what[i]]
        ret.append([train, test])
    return ret 


def list2freq(x):
    ret = {}
    for _ in x:
        if _ not in ret:
            ret[_] = 1
        else:
            ret [_] += 1
    return ret

