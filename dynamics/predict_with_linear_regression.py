#
# Training set: sequence of consecutive dates
#

from time import time

from mymodule.error import *
from mymodule.vector import *
from mymodule.linealmodel import *

from mymodule.load import load_dataset
from mymodule.get_paths import tsv_path

from mymodule.utils import date2days
from mymodule.utils import days2date
from mymodule.utils import traintest
from mymodule.utils import save_data


def write_names(vector, path):
    #no incluye colnames
    aux = '\n'.join(vector[1:])
    save_data(path, aux)

def write_vector(vector, path):
    #no incluye colnames
    aux = []
    for v in vector[1:]:
        aux.append(str(v[0]))
    aux = '\n'.join(aux)
    save_data(path, aux)


P = '/home/lgonzalez/thesis/data/prediction/'

def main():
    path = tsv_path()
    names, data = load_dataset(path) #~200s
    write_names(names, P+'names')

    for l in range(1,7):
        print('len train dataset: %d' %l)
        tt = traintest(data[0], l)
        for train, test in tt:
            datatrain = [[d[i] for i in range(len(d)) if data[0][i] in train] for d in data]
            datatest = [[d[i] for i in range(len(d)) if data[0][i] in test] for d in data]
            if l == 1:
                write_vector(datatest, P+str(days2date(datatest[0][0]))+'-real')
                #print real values
            ms_bs = [lm(datatrain[0],r) for r in datatrain]
            pred = predict(ms_bs, test)
            write_vector(pred, P+str(days2date(datatest[0][0]))+'-pred-'+str(l))
            evalu = evaluate(datatest, pred)
            print(train, evalu)





if __name__ == '__main__':
    main()
#24 s. first lm
#5 s. interpolation
#0.24474000930786133

