#
# este proceso no corrio con 48GB de ram.
# llego a la iteración 5, quitando 888.549 nodos en 20 minutos, sin considerar la carga de data
# Se prueba con 128
#


files = []
files += ['20170530-pred-1', '20170530-pred-2', '20170530-pred-3', '20170530-pred-4', '20170530-pred-5', '20170530-pred-6']
files += ['20170530-pred-dd-2', '20170530-pred-dd-3', '20170530-pred-dd-4', '20170530-pred-dd-5', '20170530-pred-dd-6', '20170530-real']
files += ['20170607-pred-1', '20170607-pred-2', '20170607-pred-3', '20170607-pred-4', '20170607-pred-5', '20170607-pred-6']
files += ['20170607-pred-dd-2', '20170607-pred-dd-3', '20170607-pred-dd-4', '20170607-pred-dd-5', '20170607-pred-dd-6', '20170607-real']
files += ['20170613-pred-1', '20170613-pred-2', '20170613-pred-3', '20170613-pred-4', '20170613-pred-5', '20170613-pred-6']
files += ['20170613-pred-dd-2', '20170613-pred-dd-3', '20170613-pred-dd-4', '20170613-pred-dd-5', '20170613-pred-dd-6', '20170613-real']
files += ['20170620-pred-1', '20170620-pred-2', '20170620-pred-3', '20170620-pred-4', '20170620-pred-5', '20170620-pred-6']
files += ['20170620-pred-dd-2', '20170620-pred-dd-3', '20170620-pred-dd-4', '20170620-pred-dd-5', '20170620-pred-dd-6', '20170620-real']
files += ['20170627-pred-1', '20170627-pred-2', '20170627-pred-3', '20170627-pred-4', '20170627-pred-5', '20170627-pred-6']
files += ['20170627-pred-dd-2', '20170627-pred-dd-3', '20170627-pred-dd-4', '20170627-pred-dd-5', '20170627-pred-dd-6', '20170627-real']
files = ['prediction/'+f for f in files]

#{ch_idx: weight}
def load_weight(filepath):
    fr = open(filepath, 'r')
    data = fr.read().strip().split('\n')
    data = {i:eval(data[i]) for i in range(len(data))}
    fr.close()
    return data

flat = {}
tran = {}
for f in files:
    flat[f] = load_weight(f)
    tran[f] = {}
    print(f)





#{cs_idx:[set([direct childs]), set([transitive childs])]}
def load_lattice():
    fr = open('mylat.txt','r')
    data = fr.read().strip()
    data += '\t'
    data = data.split('\n')
    data = [d.split('\t') for d in data]
    data = {eval(d[0]):[set([eval(_) for _ in d[1].split(' ') if _]), set()] for d in data}
    return data

def get_parents(lattice):
    #i:ch_idx
    #p[i]: direct parent of i
    p = {0:[]} # con esto todos los charsets tienen padres
    for fr in lattice:
        for to in lattice[fr][0]:
            if to not in p:
                p[to] = [fr]
            else:
                p[to].append(fr)
    return p


def iterate(lattice, parents):
    todel = [k for k in lattice if not lattice[k][0]]
    for td in todel:
        childs = lattice[td][1].union(set([td]))
        #todos tus transitivos mas tu mismo son los nodos a considerar
        for f in files:
            tran[f][td] = sum([flat[f][c] for c in childs])
        #subo mis transitivos y yo mismo a mis padres
        for p in parents[td]:
            lattice[p][1] = lattice[p][1].union(childs)
            lattice[p][0].remove(td)
        del lattice[td]
        del parents[td]


from time import time
lat = load_lattice()
par = get_parents(lat)

c = 0
prev_len = len(lat)
while lat:
    ti = time()
    iterate(lat, par)
    tf = time()
    print(c, tf-ti, prev_len - len(lat))
    prev_len = len(lat)
    c += 1



for f in tran:
    buff = [str(tran[f][i] for i in range(len(tran[f]))]
    buff = '\n'.join(buff)
    fw = open(f+'-trans')
    fw.write(buff)
    fw.close()

