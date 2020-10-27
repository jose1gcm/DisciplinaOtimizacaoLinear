# -*- coding: utf-8 -*-

from mip.model import *

model = Model("Exemplo 2")

# dados de entrada
F = [ 0, 1, 2 ]
M = [ 0, 1, 2, 3 ]
c = [ [ 0.90, 1.00, 1.80, 1.05 ], 
      [ 2.10, 0.80, 0.70, 1.15 ], 
      [ 1.10, 1.00, 1.20, 1.50 ]  ]
p = [ 22500, 21000, 19500 ]
d = [ 10000, 15000, 11000, 10000 ]

# criando variáveis
x = [ [ model.add_var() for j in M ] for i in F ]

# criando a função objetivo
model += xsum(c[i][j]*x[i][j] for i in F for j in M)

# adicionando as restrições
for i in F:
    model += xsum(x[i][j] for j in M) <= p[i]
for j in M:
    model += xsum(x[i][j] for i in F) >= d[j]

# resolvendo o modelo
model.optimize()

# imprimindo a solução
print("\n-----------------------------------")
print("Solução ótima com custo: {}\n".format(model.objective_value))
for i in F:
    for j in M:
        print("x({},{}) = {}".format(i, j, x[i][j].x))
print("-----------------------------------\n")