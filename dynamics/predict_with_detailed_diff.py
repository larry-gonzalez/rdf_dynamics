###############################
# predict with detailed delta #
###############################

from mymodule.get_paths import DATES
from mymodule.get_paths import get_detailed_diff_path
from mymodule.get_paths import get_transformed_charset_path
from mymodule.load import load_detailed_diff
from mymodule.load import load_transformed_charset
from mymodule.utils import traintest
from mymodule.utils import days2date
from mymodule.utils import save_data
from mymodule.error import rmse
from mymodule.error import mae

from mymodule.get_paths import tsv_path
from mymodule.load import load_dataset
from mymodule.utils import date2days
from mymodule.linealmodel import evaluate
from mymodule.vector import substract



def load_diff(d1,d2):
    path = get_detailed_diff_path(d1, d2)
    diff = load_detailed_diff(path)
    return diff

def tran_diff(diff):
    aux = {}
    for f,t,n in diff:
        if f not in aux:
            aux[f] = n
        else:
            aux[f] += n
    ret = []
    for f,t,n in diff:
        ret.append([f,t,n/aux[f]])
    return ret

def get_diff(d1,d2):
    diff = load_diff(d1,d2)
    tran = tran_diff(diff)
    return tran

def get_mean_diff(train):
    #load diffs
    #compute average of diffs
    #return [[from, to, mean(diffs)], ...]
    l = len(train)-1
    mean = {}
    for i in range(l):
        di, df = train[i:i+2]
        diff = get_diff(di,df)
        for f,t,v in diff:
            if f not in mean:
                mean[f] = {t:[v]}
            else:
                if t not in  mean[f]:
                    mean[f][t] = [v]
                else:
                    mean[f][t].append(v)
    ret = []
    for f in mean:
        for t in mean[f]:
            ret.append([f,t,sum(mean[f][t])/l])
    #ret = [_ for _ in ret if _[2] != 0]
    return ret 

def write_vector(vector, path):
    aux = [str(v) for v in vector]
    aux = '\n'.join(aux)
    save_data(path, aux)


P = '/home/lgonzalez/thesis/data/prediction/'


def main():
    path = tsv_path()
    names, data = load_dataset(path) #~200s

    for l in range(2,7):
        print('len diffs: %d' %l)
        tt = traintest(DATES, l)
        for train, test in tt:
            #print(train, test)
            diff = get_mean_diff(train) #[[from, to, percentaje],]
            test2 = [date2days(t) for t in test]
            last = [[d[i] for i in range(len(d)) if data[0][i] in test2] for d in data]
            last = [l[0] for l in last[1:]]#delete first element and transform list into numbers
            pred = list(last) #create a copy
            for f,t,v in diff:
                if f != t:
                    pred[f] -= v*last[f]
                    pred[t] += v*last[f]
            #pred = [round(max(0,v)) for v in pred]
            pred = [round(v) for v in pred]
            pred[0] = 0 #los que fueron eliminados
            write_vector(pred, P+str(test[0])+'-pred-dd-'+str(l))
            error = substract(pred, last)
            out = [test2[0], round(rmse(error),4), round(mae(error), 4)]
            print([date2days(t) for t in train], out)



if __name__ == '__main__':
    main()
