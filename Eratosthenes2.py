# -*- coding: utf-8 -*-
# 递归实现无改进
import sys
import time
import math

def primes(n):      # find the prime numbers in range(1,n+1)
    n = int(n)
    assert(n > 0)
    if n == 1:
        return []         
    if n == 2:
        return [2]
        
    f = [False, True] 
    f.extend([True, False]*int(n/2-1))
    if n % 2 == 1:   
        f.append(True)
    
    sp = primes(int(math.sqrt(n)))
    for each in sp[1:]:
        base = each*each
        while base < n:
            f[base-1] = False
            base += each

    P = []
    P.append(2)
    for i in range(3,n,2):
        if f[i-1]:
            P.append(i)
    return P

start = time.clock()  
#N = sys.argv[1] 
primes(641)
print(primes(641))