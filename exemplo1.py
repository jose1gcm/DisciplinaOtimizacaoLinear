# -*- coding: utf-8 -*-

from mip.model import *

model = Model("Exemplo 1", MAXIMIZE)

# criando variáveis
x1 = model.add_var()
x2 = model.add_var()

# criando a função objetivo
model += 100*x1 + 112*x2
#model.

# adicionando as restrições
model += 6*x1 + 4*x2 <= 18
model += x1 >= 1
model += x2 >= 1

# resolvendo o modelo
model.optimize()

# imprimindo a solução
print("x1 = {x1.x}, x2 = {x2.x}".format(**locals()))
print("custo:{}".format(model.objective_value))
