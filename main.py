# main.py

from generation import ModularGraph, ExtendedModularGraph
import visualisation as viz


def test_discrete_graph():
    print("\n=== Testing ModularGraph ===")

    primes = [3, 5, 7, 11]
    A = 6

    G = ModularGraph(primes, A)

    print("Graph:", G)
    print("Primes:", G.primes())
    print("Exponent:", G.exp())
    print("Order matrix:", G.order_matrix())
    print("Adjacency:", G.adjacency())
    print("Is extended?", G.is_extended())

    viz.plot(G)


def test_extended_graph():
    print("\n=== Testing ExtendedModularGraph ===")

    primes = [3, 5, 7, 11]
    A = 6

    G_ext = ExtendedModularGraph(primes, A)

    print("Graph:", G_ext)
    print("Primes:", G_ext.primes())
    print("Exponent:", G_ext.exp())
    print("Order matrix:", G_ext.order_matrix())
    print("Is extended?", G_ext.is_extended())

    # mostrar alguns pesos
    weights = G_ext.weights()
    print("Sample weights:")
    for p in primes:
        for q in primes:
            if p != q:
                print(f"w({p}->{q}) =", weights[p][q])
        break

    viz.plot(G_ext)


def test_algebra():
    print("\n=== Testing Algebraic Operations ===")

    primes = [3, 5, 7, 11]

    G1 = ModularGraph(primes, 6)
    G2 = ModularGraph(primes, 10)

    print("G1:", G1)
    print("G2:", G2)

    G_union = G1.union(G2)
    G_inter = G1.intersection(G2)
    G_comp = G1.complement()

    print("Union exponent:", G_union.exp())
    print("Intersection exponent:", G_inter.exp())
    print("Complement exponent:", G_comp.exp())

    viz.plot(G_union)
    viz.plot(G_inter)
    viz.plot(G_comp)


def main():
    test_discrete_graph()
    test_extended_graph()
    test_algebra()


if __name__ == "__main__":
    main()
