# visualisation.py

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np


def plot(G, layout="spring", show_labels=True):

    import matplotlib.pyplot as plt
    import numpy as np
    import networkx as nx

    fig, ax = plt.subplots()

    nxG = nx.DiGraph()

    for p in G.primes():
        nxG.add_node(p)

    
    
    if G.is_extended():

       weights = G.weights()
       orders = G.order_matrix()
       pos = _compute_layout(nxG, layout)

       nx.draw_networkx_nodes(nxG, pos, node_size=800, ax=ax)
       nx.draw_networkx_labels(nxG, pos, ax=ax)

       for p in weights:

           neighbors = list(weights[p].keys())
           n = len(neighbors)

           # distribuir curvatura simetricamente
           curvatures = np.linspace(-0.4, 0.4, n)

           for idx, q in enumerate(neighbors):

               ratio = G.exp() / orders[p][q]

               nx.draw_networkx_edges(
                nxG,
                pos,
                edgelist=[(p, q)],
                connectionstyle=f"arc3,rad={curvatures[idx]}",
                arrows=True,
                ax=ax
            )

               if show_labels:
                w_complex = weights[p][q]

                real = round(w_complex.real, 2)
                imag = round(w_complex.imag, 2)

                if imag >= 0:
                  label = f"{real}+{imag}i"
                else:
                    label = f"{real}{imag}i"
                nx.draw_networkx_edge_labels(
    nxG,
    pos,
    edge_labels={(p, q): label},
    font_size=8,
    ax=ax
)

       ax.set_title(
        f"Extended Modular Graph (A={G.exp()})\n"
        "Edge label = w(pi,pj)"
    )

    else:

        for p, neighbors in G.adjacency().items():
            for q in neighbors:
                nxG.add_edge(p, q)

        pos = _compute_layout(nxG, layout)

        nx.draw(
            nxG,
            pos,
            with_labels=True,
            arrows=True,
            ax=ax
        )

        ax.set_title(f"Modular Graph (A={G.exp()})")

    plt.show()

def _compute_layout(G, layout):

    if layout == "spring":
        return nx.spring_layout(G)
    elif layout == "circular":
        return nx.circular_layout(G)
    elif layout == "kamada":
        return nx.kamada_kawai_layout(G)
    else:
        return nx.spring_layout(G)
def plot_spectrum(G_ext):
    import numpy as np

    P = G_ext.primes()
    weights = G_ext.weights()

    n = len(P)
    M = np.zeros((n, n), dtype=complex)

    for i, p in enumerate(P):
        for j, q in enumerate(P):
            if p != q:
                M[i][j] = weights[p][q]

    eigenvalues = np.linalg.eigvals(M)

    plt.figure()
    plt.scatter(eigenvalues.real, eigenvalues.imag)
    plt.axhline(0)
    plt.axvline(0)
    plt.title("Spectrum")
    plt.xlabel("Real")
    plt.ylabel("Imaginary")
    plt.show()
