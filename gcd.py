# -*- coding: utf-8 -*-
def GCD(rj_2, rj_1, sj_2, sj_1, tj_2, tj_1): # get sj, tj and rj
    if rj_1 == 0: #j starts from 2, stops when j equals n+2
        return sj_2, tj_2, rj_2
    qj_1 = int(rj_2 / rj_1)
    rj = rj_2 - qj_1*rj_1
    sj = sj_2 - qj_1*sj_1
    tj = tj_2 - qj_1*tj_1
    return GCD(rj_1, rj, sj_1, sj, tj_1, tj)

def gcd(a, b): # wrapper
    if a > b:
    	return GCD(a, b, 1, 0, 0, 1)
    return GCD(b, a, 1, 0, 0, 1)
a=47
b=34
print(gcd(b, a))

    

