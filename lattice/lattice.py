import sys
from time import time



input_file   = sys.argv[1]
output_file  = sys.argv[2]
perform_file = sys.argv[3]

#print(perform_file)


fr = open(input_file)

#{i:charset}
charsets = fr.read().strip().split('\n')
charsets = [frozenset(eval(cs)) for cs in charsets]
charsets.append(frozenset([])) #starting point
charsets.sort(key = lambda x: len(x))
charsets = {i:charsets[i] for i in range(len(charsets))}
fr.close()

#[predicate]
preds = [pred for idx in charsets for pred in charsets[idx]]
preds = list(set(preds))
preds.sort()

#{pred: frequency}
pred_freq = {p:0 for p in preds}
for idx in charsets:
    for pred in charsets[idx]:
        pred_freq[pred] += 1




#[charsets_length]
levels = list(set([len(charsets[idx]) for idx in charsets]))
levels.sort()

#{level: [charset_idx]}
level_charsets = {l:[idx for idx in charsets if len(charsets[idx])==l] for l in levels}

#{level: {pred: [charset_idx]}}
level_inverted_index = {}
for l in levels:
    mydict = {pred:[] for pred in preds} #need to have an empty list (base case)
    mycharsets = level_charsets[l]
    for idx in mycharsets:
        for pred in charsets[idx]:
             mydict[pred].append(idx)
    level_inverted_index[l] = mydict

#charset -> predicate
def less_freq(myfrozenset):
    #assumes pred_freq #!!!
    less_freq = 0
    curr_freq = float('inf')
    for s in myfrozenset:
        if pred_freq[s] < curr_freq:
            less_freq = s
            curr_freq = pred_freq[s]
    return less_freq



#{level: {rarest_pred: [charset_idx]}}
level_rarest_inverted_index = {}
for l in levels[1:]:
    mydict = {}
    css_idx = level_charsets[l]
    for idx in css_idx:
        rarest = less_freq(charsets[idx])
        if rarest in mydict:
            mydict[rarest].append(idx)
        else:
            mydict[rarest] = [idx]
    level_rarest_inverted_index[l] = mydict




class Graph:
    def __init__(self):
        self.edges = {}
    def add_node(self, n):
        if n not in self.edges:
            self.edges[n] = {}
    def add_edge(self, n1, n2):
        #it assumes n1 and n2 in edges#
        self.edges[n1][n2]=None
    def successors(self,n):
        return self.edges[n]
    def len(self):
        r = 0
        for n in self.edges:
            r += len(self.edges[n])
        return r

def has_path(g, source, target):
    #assumes charsets
    aux = g.successors(source)
    if target in aux:
        return True
    for n in aux:
        if charsets[n].issubset(charsets[target]):
            return True
    return False

def diff_level_1(g, li, lj):
    css_idx_li = level_charsets[li]
    css_idx_lj = level_charsets[lj]
    css_idx_lj = {charsets[_]:_ for _ in css_idx_lj} #inverted dict {charset: charset_idx}
    for cs_idx_li in css_idx_li:
        cs_li = charsets[cs_idx_li]
        for pred in cs_li:
            new_cs = cs_li - frozenset([pred])
            if new_cs in css_idx_lj:
                g.add_edge(css_idx_lj[new_cs], cs_idx_li)

def diff_general(g, li, lj):
    rarest_pred_lj = level_rarest_inverted_index[lj]
    for pred_lj in rarest_pred_lj:
        #nodes_li are nodes to be added
        nodes_lj_idx = level_rarest_inverted_index[lj][pred_lj]
        nodes_li_idx = level_inverted_index[li][pred_lj]
        for nj_idx in nodes_lj_idx:
            for ni_idx in nodes_li_idx:
                if charsets[nj_idx].issubset(charsets[ni_idx]) and \
                    not has_path(g, nj_idx, ni_idx):
                    g.add_edge(nj_idx, ni_idx)



g = Graph()
for cs_idx in charsets:
    g.add_node(cs_idx)


fw = open(perform_file, 'w')
for i in range(1, len(levels)):    # the level index of adding nodes
    #for i in range(1, 15):
    for j in range(i-1, -1, -1): # the level index of comparing nodes
        # li > lj
        ti = time()
        li = levels[i]
        lj = levels[j]
        if lj: # not 0, not frozenset([])
            if li-lj == 1:
                diff_level_1(g, li, lj)
            else:
                diff_general(g, li, lj)
        else:
            for ni_idx in level_charsets[li]:
                if not has_path(g, 0, ni_idx):
                    g.add_edge(0, ni_idx)
        tf = time()
        garbage = fw.write('%d\t%d\t%s\n' %(i, j, str(tf-ti)))

fw.close()



fw = open(output_file, 'w')
for i in range(len(charsets)):
    for j in g.successors(i):
        n1 = str(set(charsets[i])) if i else '{}'
        n2 = str(set(charsets[j]))
        garbage = fw.write('%s\t%s\n' %(n1, n2))

fw.close()

#
# Tengo la impresión (revisar) de que esto escribe sets de predicados
#
