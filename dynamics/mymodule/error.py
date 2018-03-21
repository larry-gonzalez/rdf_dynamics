from math import sqrt


def mae(error):
    aux = [abs(e) for e in error]
    aux = sum(aux)/len(aux)
    return aux

def rmse(error):
    aux = [e*e for e in error]
    aux = sum(aux)/len(aux)
    aux = sqrt(aux)
    return aux



if __name__ == '__main__':
    # mae
    assert mae([0]) == 0, 1
    assert mae([1,1,1,1,1,1]) == 1, 2
    assert mae([-1,1,-1,-1]) == 1, 3
    assert mae([1,2,3,4,5]) == 3, 3
    assert mae([-1,-2,3,4,5]) == 3, 3
    assert round(rmse([1,1,1,1,1]),4) == 1.0
    assert round(rmse([1,2,3,4,5]),4) == 3.3166
    assert round(rmse([-1,-2,3,4,5]),4) == 3.3166
