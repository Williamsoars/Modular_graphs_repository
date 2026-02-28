# generation.py

import math
import cmath
from sympy import gcd
from sympy.ntheory import multiplicative_order


class ModularGraph:

    def __init__(self, primes, exponent):
        self._P = sorted(primes)
        self._A = exponent
        self._order_matrix = self._compute_order_matrix()
        self._adjacency = self._generate_adjacency()

    # ==========================
    # Core Properties
    # ==========================

    def primes(self):
        return self._P

    def exp(self):
        return self._A

    def order_matrix(self):
        return self._order_matrix

    def adjacency(self):
        return self._adjacency

    # ==========================
    # Internal Computations
    # ==========================

    def _compute_order_matrix(self):
        O = {}
        for p in self._P:
            O[p] = {}
            for q in self._P:
                if p == q:
                    O[p][q] = 0
                else:
                    O[p][q] = multiplicative_order(p, q)
        return O

    def _generate_adjacency(self):
        adj = {}
        for p in self._P:
            adj[p] = []
            for q in self._P:
                if p != q:
                    if self._order_matrix[p][q] != 0:
                        if self._A % self._order_matrix[p][q] == 0:
                            adj[p].append(q)
        return adj

    # ==========================
    # Graph Operations
    # ==========================

    def union(self, other):
        lcm_exp = math.lcm(self._A, other._A)
        return ModularGraph(self._P, lcm_exp)

    def intersection(self, other):
        gcd_exp = math.gcd(self._A, other._A)
        return ModularGraph(self._P, gcd_exp)

    def complement(self):
        A_star = self._compute_complete_exponent()
        A_comp = A_star // self._A
        return ModularGraph(self._P, A_comp)

    def _compute_complete_exponent(self):
        values = [p - 1 for p in self._P]
        A_star = values[0]
        for v in values[1:]:
            A_star = math.lcm(A_star, v)
        return A_star

    # ==========================
    # Utilities
    # ==========================

    def __repr__(self):
        return f"ModularGraph(P={self._P}, A={self._A})"
