import sys
from mymodule.get_paths import all_charset_path
from mymodule.get_paths import get_raw_charset_path
from mymodule.get_paths import get_detailed_diff_path
from mymodule.load import load_all_cs_file
from mymodule.load import load_raw_charset
from mymodule.utils import save_data
from transform import transform_raw_charset


if __name__ == '__main__':
    d1 = sys.argv[1]
    d2 = sys.argv[2]
    out = get_detailed_diff_path(d1, d2)

    #dictionary of frozensets as key and cs_idx value
    #frozenset({}): 0
    all_cs = load_all_cs_file(all_charset_path())

    data1 = load_raw_charset(d1)                 #[[[preds], [subs]], ...]
    data1 = transform_raw_charset(all_cs, data1) #{sub_idx: cs_idx, ...}

    data2 = load_raw_charset(d2)
    data2 = transform_raw_charset(all_cs, data2)

    all_cs = None

    delta = {} # {cs_from:{cs_to:[subs], ...}, ...}
    for i in range(1,max(max(data1), max(data2))+1):
        if i in data1:
            cs_from = data1[i]
            del data1[i]
        else:
            cs_from = 0 #frozenset([]) # creation
        if i in data2:
            cs_to = data2[i]
            del data2[i]
        else:
            cs_to = 0 #frozenset([]) # deletion
        if cs_from not in delta:
            delta[cs_from] = {cs_to:[i]}
        else:
            if cs_to not in delta[cs_from]:
                delta[cs_from][cs_to] = [i]
            else:
                delta[cs_from][cs_to].append(i)

    buff = ''
    for f in delta:
        for t in delta[f]:
            buff += '%d\t%d\t%d\n' %(f, t, len(delta[f][t]))

    save_data(out, buff)

