import os
import bz2
import sys 
import time

"""
Assumptions:
*   all bz2 files are in the same folder
*   dictionaries will have the same name

It will use previous dictionaries
It can also work with all files ''at the same time''
"""


DATES = [20170418, 20170425, 20170503, 20170509, 20170516, 20170524, 20170530,
20170607, 20170613, 20170620, 20170627]
DATES = [20170418, 20170425]
DATES = [str(d) for d in DATES]


def load_dict(path):
    """the number of the line is the id of the dictionary starting with 0"""
    ret = {}
    if os.path.isfile(path):
        fr = open(path, 'r')
        c = 0
        for line in fr:
            ret[line.strip()] = c
            c += 1
        fr.close()
    return(ret)



def get_spo(line):
    """returns a list of three elements: subject, predicate and object"""
    line = str(line)
    line = line[2:]
    line = line.strip()
    sp1 = line.find(' ')
    sp2 = line.find(' ', sp1+1)
    return [line[:sp1], line[sp1+1:sp2], line[sp2+1:-2]]



if __name__ == '__main__':
    """If dictionary exists, this script will append results.
    We asume a correct Usage:
    python3.5 nt2num.py inp=input.nt out=out.nt sub=sub.file pre=pre.file obj=obj.file
    """

    subs = load_dict('sub-dict.txt')
    pres = load_dict('pre-dict.txt')
    fa_subs = open('sub-dict.txt', 'a')
    fa_pres = open('pre-dict.txt', 'a')

    for d in DATES:
        print(time.time(), 'starting', d)
        print('subs dic size', len(subs))
        print('pres dic size', len(pres))
        fp = 'wikidata-' + d + '-truthy-BETA.nt.bz2'  # file path
        fr = bz2.open(fp, "r")                        # file to read
        fw = d + '-s-p.txt'                           # file to write
        fw = open(fw,'w')                             # file to write
        for line in fr:
            s,p,o = get_spo(line)
            #check if s is in the dictionary
            if s not in subs:
                si = len(subs)
                subs[s] = si
                fa_subs.write(s+'\n')
            else:
                si = subs[s]
            #check if p is in the dictionary
            if p not in pres:
                pi = len(pres)
                pres[p] = pi
                fa_pres.write(p+'\n')
            else:
                pi = pres[p]
            fw.write('%d %d\n' %(si, pi))

        fw.close()
    print(time.time(), 'ending')
    print('subs dic size', len(subs))
    print('pres dic size', len(pres))

    fa_subs.close()
    fa_pres.close()


