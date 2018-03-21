from mymodule.error import *
from mymodule.vector import *


def lm(x,y):
    assert len(x) == len(y), 'lm error'
    L = len(x)
    mx = sum(x)/L
    my = sum(y)/L
    num = [(x[i]-mx)*(y[i]-my)for i in range(L)]
    den = [(x[i]-mx)*(x[i]-mx)for i in range(L)]
    num = sum(num)
    den = sum(den)
    m = float(num)/den if den else 0.0
    b = my - m*mx
    return(m,b)

def predict(m_b, x):
    ret = []
    for mb in m_b:
        cur = [int(round(mb[0]*_+mb[1])) for _ in x]
        cur = [c if c> 0 else 0 for c in cur]
        ret.append(cur)
    return(ret)

def evaluate(real, pred):
    assert len(real) == len(pred), 'evaluate error: 1'
    #assert real[0] == pred[0], 'evaluate error: 2'
    myreal = [list(_) for _ in list(zip(*real))]
    mypred = [list(_) for _ in list(zip(*pred))]
    ret = []
    for i in range(len(myreal)):
        d = myreal[i][0]
        cr = myreal[i][1:]
        cp = mypred[i][1:]
        error = rest(cr, cp)
        cur = [d, round(rmse(error),4), round(mae(error), 4)]
        ret.append(cur)
    return(ret)

