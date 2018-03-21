from mymodule.utils import str2list
from mymodule.utils import date2days
from mymodule.get_paths import get_raw_charset_path



def load_raw_charset(date):
    """[[predicates], [subjects]]"""
    fr = open(get_raw_charset_path(date), 'r')
    data = fr.read().strip().split('\n') # list of strings
    data = [d.split('\t') for d in data] # list of lists of strings
    for i in range(len(data)):
        #this way is for memory efficiency
        data[i][0] = eval(data[i][0])     # list of predicates
        data[i][1] = str2list(data[i][1]) # list of subjects
    return data


def load_simplified_charset(filepath):
    #[[frozenset(...), num_of_subjects], ...]
    fr = open(filepath, 'r')
    data = fr.read().strip().split('\n')
    data = [d.split('\t') for d in data]
    data = [[frozenset(eval(d[0])), eval(d[1])] for d in data]
    return data


def load_transformed_charset(filepath):
    fr = open(filepath, 'r')
    data = fr.read().strip().split('\n')
    data = [d.split('\t') for d in data]
    data = [[int(d[0]), int(d[1])] for d in data]
    return data


def load_dataset(filepath):
    #return matrix dataset.tsv
    #we decided to consider first 11 datasets.
    fr = open(filepath, 'r')
    data = fr.read().strip().split('\n')
    data = [d.split('\t') for d in data]
    names = [d[0] for d in data]
    data = [d[1:] for d in data]
    data = [[eval(v) for v in row ] for row in data]
    data[0] = [date2days(_) for _ in data[0]]
    return names, data


def load_all_cs_file(filepath):
    #{frozenset:num}
    fr = open(filepath, 'r')
    data = fr.read().strip().split('\n')
    #data = {eval(data[i]):i for i in range(len(data))}
    data = {frozenset(eval(data[i])):i+1 for i in range(len(data))}
    data[frozenset():0]
    return data




def load_detailed_diff(filepath):
    #return [[from, to, n], ...]
    #consider that 'from' and 'to' can be 'creation' or 'deletion'
    #2017-10-20 from and to are only numbers
    #2017-10-20 from and to 0 means creation and deletion
    #always 0 is included as frozenset({})
    fr = open(filepath, 'r')
    data = fr.read().strip().split('\n')
    data = [d.split('\t') for d in data]
    data = [[eval(v) for v in d] for d in data]
    return data



