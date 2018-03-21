
#####################
# VECTOR OPERATIONS #
#####################

def add(v1, v2):
    assert len(v1) == len(v2), 'add error'
    ret = [v1[i]+v2[i] for i in range(len(v1))]
    return ret

def substract(v1, v2):
    assert len(v1) == len(v2), 'substract error'
    ret = [v1[i]-v2[i] for i in range(len(v1))]
    return ret

def mult(v1, v2):
    assert len(v1) == len(v2), 'mult error'
    ret = [v1[i]*v2[i] for i in range(len(v1))]
    return ret


################################
# VECTOR AND SCALAR OPERATIONS #
################################

def add_scalar(vector, scalar):
    ret = [v + scalar for v in vector]
    return ret

def substract_scalar(vector, scalar):
    ret = [v - scalar for v in vector]
    return ret

def mult_scalar(vector, scalar):
    ret = [v * scalar for v in vector]
    return ret

