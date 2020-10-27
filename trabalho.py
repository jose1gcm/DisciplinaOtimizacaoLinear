# -*- coding: utf-8 -*-

import math
from mip import *
import networkx as nx

EPS = 1e-4
F = None   # variável global auxiliar

def main():
    # coordenadas das cidades
    points = [
        (77, 25),    (50, 45),     (65, 79),    (9, 2),
        (84, 43),    (76, 0),      (44, 72),    (23, 95),
        (10, 67),    (29, 50),     (13, 50),    (11, 15),
        (29, 32),    (277, 25),    (250, 45),   (265, 79),
        (29, 2),     (284, 43),    (276, 0),    (144, 72),
        (223, 95),   (210, 67),    (229, 50),   (13, 150),
    ]
    n = len(points) # nro de cidades

    # calculando distancias euclidianas
    dist = {(i,j) :
        math.sqrt(sum((points[i][k]-points[j][k])**2 for k in range(2)))
        for i in range(n) for j in range(n) if i != j}

    # criando o modelo inicial
    model = Model()

    # criando variáveis X
    x = {(i,j) :
        model.add_var(var_type=BINARY, name='x_{i}_{j}'.format(**locals()))
        for i in range(n) for j in range(n) if i != j}

    # criando variáveis U
    u = {i: model.add_var(ub=n, name='y_{i}'.format(**locals())) for i in range(n)}

    # criando função objetivo
    model += xsum(dist[i,j]*x[i,j] for i in range(n) for j in range(n) if i != j)

    # criando restrições de in/out
    for i in range(n):
        model += xsum(x[i,j] for j in range(n) if i != j) == 1
        model += xsum(x[j,i] for j in range(n) if i != j) == 1

    # criando restrições MTZ
    u[0] = 1
    for i in range(n):
        for j in range(1,n):
            if i != j:
                model += u[i] - u[j] + n*x[i,j] <= n - 1

    model.relax() # relaxando as restrições de integralidade
    has_cut = True
    while has_cut:
        model.optimize()
        print('\nCusto da solução relaxada: %.5f' % model.objective_value)

        n_cuts = 0
        nodes_list = subtours(n, dist, model, x)
        for nodes in nodes_list:
            if len(nodes) < n:
                arcs = [(i,j) for (i,j) in dist if i in nodes and j in nodes]
                print('\nCorte adicionado:\n ' + ' + '.join([x[i,j].name for (i,j) in arcs]), '<=', len(nodes) - 1)
                model += xsum(x[i,j] for (i,j) in arcs) <= len(nodes) - 1
                n_cuts += 1
        
        print('\nTotal de cortes:', n_cuts, '\n')
        has_cut = n_cuts > 0

    print('Custo da solução final: %.3f' % model.objective_value)

def subtours(n, dist, model, x):
    # construindo grafo auxiliar (apenas uma vez)
    global F
    if not F:
        F = []
        G = nx.DiGraph()
        for ((i, j), val) in dist.items():
            G.add_edge(i, j, weight=val)
        for i in range(n):
            P, D = nx.dijkstra_predecessor_and_distance(G, source=i)
            DS = list(D.items())
            DS.sort(key=lambda x: x[1])
            F.append((i, DS[-1][0]))

    G = nx.DiGraph()
    for (i, j) in x.keys():
        if x[(i,j)].x > EPS:
            G.add_edge(i, j, capacity=x[i,j].x)

    cycles = set()
    for (u, v) in F:
        val, (S, NS) = nx.minimum_cut(G, u, v)
        if len(S) > 1 and len(S) < n and val <= 0.99:
            arcs_S = [(i,j) for (i,j) in dist if i in S and j in S]
            if sum(x[arc].x for arc in arcs_S) >= len(S) - 1 + EPS:
                cycles.add(tuple(S))

    return cycles

if __name__ == "__main__":
    main()
