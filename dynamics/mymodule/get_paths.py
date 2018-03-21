#############################################
# IT IS NECESARY TO COMENT ONE OF FOLLOWING #
#############################################
BASE = '/home/lgonzalez/thesis/data/'
#BASE = '/media/lgonzalez/S1/thesis/data/'


#DATES = [20170418, 20170425, 20170503, 20170509, 20170516, 20170524, 20170530, 20170607, 20170613, 20170620, 20170627, 20170712, 20170718, 20170725]
DATES = [20170418, 20170425, 20170503, 20170509, 20170516, 20170524, 20170530, 20170607, 20170613, 20170620, 20170627]


def __get_raw_charset__(date, sufix=''):
    return BASE + 'chsets/%s-uc.txt%s' %(str(date), sufix)

def get_raw_charset_path(date):
    return __get_raw_charset__(date)

def get_raw_charset_path_preds(date):
    return __get_raw_charset__(date, '-pre')

def get_raw_charset_path_subs(date):
    return __get_raw_charset__(date, '-sub')

def get_simplified_charset_path(date):
    return __get_raw_charset__(date, '-simplified')

def get_transformed_charset_path(date):
    return __get_raw_charset__(date, '-transformed')


def all_charset_path():
    return BASE + 'chsets/all_charsets.txt'

def tsv_path(partial=False):
    ret = BASE + 'chsets/dataset.tsv'
    if partial:
        ret += '_partial'
    return ret

def get_detailed_diff_path(date1, date2):
    return BASE + 'diff/%s-%s.txt' %(date1, date2)

def get_lattice_diff_path(date1, date2):
    return BASE + 'diff/lattice-%s-%s.txt' %(date1, date2)
