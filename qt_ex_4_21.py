#!/usr/bin/env python

""" 
This file implements calculations related to modeling probabilities
for cyclic queues, which are simplified closed Jackson networks.

Given a set of system parameters for each node in the 
network (mu, # of servers) we can calculate probabilities of a 
state vector corresponding to the number of customers at each
node in the network.

Specifically, this file was implemented to double-check arithmetic
done to solve problem 4.21 in Gross et al.
"""

import itertools as it
import numpy as np
from math import factorial

def a(n_vec, c_vec):
    to_return = []
    for idx, n in enumerate(n_vec):
        c = c_vec[idx]
        if n < c:
            to_return.append(factorial(n))
        else:
            to_return.append(c**(n-c)*factorial(c))
    return to_return

""" 
Arguments: N = number of machines, 
           k = number of nodes,
           mu_vec = list of mu's for nodes 
           c_vec = list of c's for nodes 
"""
def cyclic_G(N, mu_vec, c_vec):
    k = len(mu_vec)
    # Find permutations of node states (tuples that sum to N)
    p = filter(lambda x: sum(x) == N, 
               list(it.permutations(range(N+1), k)))

    # Assume k >= 2 (network) and that vecs have length k
    total = 0
    
    # Want to sum over all the permutations of node states
    for t in p:
        numerator = float(mu_vec[0]**(N-t[0]))
        denominator = float(np.product(np.power(mu_vec[1:],t[1:])))
        quotient = numerator/denominator
        
        # Now calculate \prod_i a_i(n_i)
        prod_a = np.product(a(t, c_vec))
        to_sum = quotient/prod_a

        total += to_sum

    return total

"""
Calculates the probability of a system state vector (n_vec) given
a vector of mu's and server count for each node in the network.
"""
def prob_n_vec(N, n_vec, mu_vec, c_vec):
    numerator = float(mu_vec[0]**(N-n_vec[0]))
    denominator = float(np.product(np.power(mu_vec[1:], n_vec[1:])))
    quotient = numerator/denominator
    prod_a = np.product(a(n_vec, c_vec))
    
    return (quotient/prod_a)*(1/cyclic_G(N, mu_vec, c_vec))

if __name__ == "__main__":
    mu_vec = [ 0.1, 0.2 ]
    c_vec = [5, 2]
    N = 5

    p = filter(lambda x: sum(x) == N, 
               list(it.permutations(range(N+1), len(mu_vec))))
    
    
    total = 0.0

    for t in p:
        prob = prob_n_vec(N, t, mu_vec, c_vec)
        print t, ":", prob
        total += prob 

    print "Sum of probabilities: ", total
    print "G(5) = ", cyclic_G(N, mu_vec, c_vec)    
