#######################################################################################################################                                                                                  #
#               PercoMCV code source, implemented by the www.abil.ac.cd composed by Elie Mayogha,                     #
#                       Selain Kasereka, Nathanael Kasoro, Ho Tuong Vinh and Joel Kinganga                            #
#                                                                                                                     #
#       We invite contributor to reuse our code source and cite our paper. We would like to be contacted when         #
#       this code is used, this way will allow us to know the evolution of our proposed algorithm. Injoy              #
#                                   Contact us: contact@abil.ac.cd - University of Kinshasa                           #                        #
####################################################################################################################### 

# -*- coding: utf-8 -*-

from collections import defaultdict
import networkx as nx

# First step
# computation of k-clique percolation algorithm
# with k = 4

def k_clique_communities(G, cliques=None):
    if cliques is None:
        cliques = nx.find_cliques(G)
    cliques = [frozenset(c) for c in cliques if len(c) >= 4]

    # First index which nodes are in which cliques
    membership_dict = defaultdict(list)
    for clique in cliques:
        for node in clique:
            membership_dict[node].append(clique)

    # For each clique, see which adjacent cliques percolate
    perc_graph = nx.Graph()
    perc_graph.add_nodes_from(cliques)
    for clique in cliques:
        for adj_clique in _get_adjacent_cliques(clique, membership_dict):
            if len(clique.intersection(adj_clique)) >= 3:
                perc_graph.add_edge(clique, adj_clique)

    # Connected components of clique graph with perc edges
    # are the percolated cliques
    for component in nx.connected_components(perc_graph):
        yield (frozenset.union(*component))


def _get_adjacent_cliques(clique, membership_dict):
    adjacent_cliques = set()
    for n in clique:
        for adj_clique in membership_dict[n]:
            if clique != adj_clique:
                adjacent_cliques.add(adj_clique)
    return adjacent_cliques

# Zachary's Karate club example
Graphe = [(1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9), (1, 11), (1, 12), (1, 13),
          (1, 14), (1, 18), (1, 20), (1, 22), (1, 32), (2, 3), (2, 4), (2, 8), (2, 14), (2, 18),
          (2, 20), (2, 22), (2, 31), (3, 4), (3, 8), (3, 9), (3, 10), (3, 14), (3, 28), (3, 29),
          (3, 33), (4, 8), (4, 13), (4, 14), (5, 7), (5, 11), (6, 7), (6, 11), (6, 17), (7, 17),
          (9, 31), (9, 33), (9, 34), (10, 34), (14, 34), (15, 33), (15, 34), (16, 33), (16, 34),
          (19, 33), (19, 34), (20, 34), (21, 33), (21, 34), (23, 33), (23, 34), (24, 26), (24, 28),
          (24, 30), (24, 33), (24, 34), (25, 26), (25, 28), (25, 32), (26, 32), (27, 30), (27, 34),
          (28, 34), (29, 32), (29, 34), (30, 33), (30, 34), (31, 33), (31, 34), (32, 33), (32, 34),
          (33, 34)]
H = nx.Graph(Graphe)
c = list(k_clique_communities(H))
# cliques = nx.find_cliques(G)


m2 = set([Graphe[1][0]])
print("Temporary community : \n")
coms = []
for com in c:
    Coms = list(com)
    print(len(Coms))
    coms += [Coms]
    m1 = set(Coms)

    m2 = m2 | m1
    print(sorted(Coms))

print("------------------------")

print("******************************************")

t = []
p = 1
while p <= len(H.nodes):
    t.append(p)
    p += 1
t = set(t)
NodnClasses = t - m2
print("Unclassified node(s):\n")
print(len(NodnClasses))
print(sorted(NodnClasses))
print("******************************************")

# Second step
# Trying to classify unclassified nodes7

NodnClasses = sorted(NodnClasses)

print("                                           ")

print("******************************************")

for Com in range(len(coms)):
    print(Com)
    if len(coms[Com]) > 3:  # Check si la communauté à plus de 3 noeud

        G = H.subgraph(coms[Com])
        Nnod = G.number_of_nodes

        # Calcul de la centralité de vecteur propre
        centrality = nx.eigenvector_centrality(G)
        vercteur_pr = sorted((round((centrality[node]), 2), node) for node in centrality)
        for vect in range(len(vercteur_pr)):
            centralitiness = vercteur_pr[vect][0] / vercteur_pr[len(vercteur_pr) - 1][0]
            print(str(vercteur_pr[vect][1]) + " Is as central as " + str(
                vercteur_pr[len(vercteur_pr) - 1][1]) + " at " + str(round(centralitiness * 100, 2)) + "%")
            if centralitiness >= 0.99:  # check if the node is 99% central
                neud_central = vercteur_pr[vect][1]
                # print(vercteur_pr[vect][0])
                for nod in range(len(NodnClasses)):
                    if H.has_edge(NodnClasses[nod], neud_central):
                        coms[Com] += [NodnClasses[nod]]

print("Final Communities detected")
print("******************************************")
colors = ['b', 'g', 'y', 'b']
pos = nx.spring_layout(H)
cc = []
for i in range(len(coms)):
    print("Community #" + str(i + 1) + "")
    print(sorted(set(coms[i])))
    cc += coms[i]
    # nx.draw(H,pos=nx.spring_layout(H),nodelist= coms[i])
    fG = H.subgraph(coms[i])
    nx.draw(fG, pos, nodelist=coms[i], with_labels=True, node_color=colors[i])
    # nx.draw_networkx_edges(fG,pos,width=1.0,alpha=0.5)
    plt.show()
cc = sorted(set(cc))
FinalUnclass = list(t - set(cc))
print("Final unclassified node(s)")
print(FinalUnclass)

####################################################################################################################### 


