from mymodule.get_paths import get_transformed_charset_path
from mymodule.get_paths import all_charset_path
from mymodule.get_paths import DATES
from mymodule.get_paths import tsv_path
from mymodule.utils import save_data
from mymodule.load import load_all_cs_file
from mymodule.load import load_transformed_charset
from time import time


if __name__ == '__main__':
    """create dataset.tsv. Matrix with charsets vs dates"""
    cs = load_all_cs_file(all_charset_path()) #fronzenset:num
    cs = {cs[c]:c for c in cs} #num:frozenset
    cs = [str(cs[i]) for i in range(len(cs))]

    ret = []
    for date in DATES:
        ti = time()
        path = get_transformed_charset_path(date)
        data = load_transformed_charset(path)
        cur = [0]*len(cs)
        for d in data:
            cur[d[0]] = d[1]
        cur = [str(c) for c in cur]
        cur.insert(0, str(date))
        ret.append(cur)
        tf = time()
        print(tf-ti, date)

    cs.insert(0, 'charset')
    ret.insert(0, cs)
    ret = [list(_) for _ in zip(*ret)]
    ret = ['\t'.join(r) for r in ret]
    ret = '\n'.join(ret)
    save_data(tsv_path(), ret)



