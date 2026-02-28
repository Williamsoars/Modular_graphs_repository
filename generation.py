# generation.py

import math
import cmath


# ============================================================
# Utility: multiplicative order (sem sympy)
# ============================================================

def multiplicative_order(a, p):
    """
    Retorna a ordem multiplicativa de a modulo p,
    assumindo p primo e gcd(a, p) = 1.
    """

    if math.gcd(a, p) != 1:
        return 0

    phi = p - 1

    # encontrar divisores de phi
    divisors = []
    for i in range(1, int(math.sqrt(phi)) + 1):
        if phi % i == 0:
            divisors.append(i)
            if i != phi // i:
                divisors.append(phi // i)

    divisors.sort()

    for d in divisors:
        if pow(a, d, p) == 1:
            return d

    return phi


# ============================================================
# Base Class
# ============================================================

class BaseModularGraph:

    def primes(self):
        raise NotImplementedError

    def exp(self):
        raise NotImplementedError

    def is_extended(self):
        return False

    def to_networkx(self):
        raise NotImplementedError


# ============================================================
# Discrete Modular Graph
# ============================================================

class ModularGraph(BaseModularGraph):

    def __init__(self, primes, exponent):
        self._P = sorted(primes)
        self._A = exponent
        self._order_matrix = self._compute_order_matrix()
        self._adjacency = self._generate_adjacency()

    # ----------------------

    def primes(self):
        return self._P

    def exp(self):
        return self._A

    def order_matrix(self):
        return self._order_matrix

    def adjacency(self):
        return self._adjacency

    def is_extended(self):
        return False

    # ----------------------

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
                    ord_pq = self._order_matrix[p][q]
                    if ord_pq != 0 and self._A % ord_pq == 0:
                        adj[p].append(q)
        return adj

    # ----------------------

    def union(self, other):
        if set(self._P) != set(other._P):
            raise ValueError("Prime sets must match.")
        return ModularGraph(self._P, math.lcm(self._A, other._A))

    def intersection(self, other):
        if set(self._P) != set(other._P):
            raise ValueError("Prime sets must match.")
        return ModularGraph(self._P, math.gcd(self._A, other._A))

    def complement(self):
        A_star = self._complete_exponent()
        return ModularGraph(self._P, A_star // self._A)

    def _complete_exponent(self):
        values = [p - 1 for p in self._P]
        A_star = values[0]
        for v in values[1:]:
            A_star = math.lcm(A_star, v)
        return A_star

    # ----------------------

    def to_networkx(self):
        import networkx as nx

        nxG = nx.DiGraph()

        for p in self._P:
            nxG.add_node(p)

        for p, neighbors in self._adjacency.items():
            for q in neighbors:
                nxG.add_edge(p, q)

        return nxG

    def __repr__(self):
        return f"ModularGraph(P={self._P}, A={self._A})"


# ============================================================
# Extended Modular Graph
# ============================================================

class ExtendedModularGraph(BaseModularGraph):

    def __init__(self, primes, exponent):
        self._P = sorted(primes)
        self._A = exponent
        self._order_matrix = self._compute_order_matrix()
        self._weights = self._generate_weights()

    # ----------------------

    def primes(self):
        return self._P

    def exp(self):
        return self._A

    def order_matrix(self):
        return self._order_matrix

    def weights(self):
        return self._weights

    def is_extended(self):
        return True

    # ----------------------

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

    def _generate_weights(self):
        weights = {}
        for p in self._P:
            weights[p] = {}
            for q in self._P:
                if p != q:
                    ord_pq = self._order_matrix[p][q]
                    if ord_pq != 0:
                        phase = self._A / ord_pq
                        weights[p][q] = cmath.exp(1j * math.pi * phase)
        return weights

    # ----------------------

    def to_networkx(self):
        import networkx as nx

        nxG = nx.DiGraph()

        for p in self._P:
            nxG.add_node(p)

        for p in self._weights:
            for q in self._weights[p]:
                nxG.add_edge(p, q, weight=self._weights[p][q])

        return nxG

    def __repr__(self):
        return f"ExtendedModularGraph(P={self._P}, A={self._A})"
