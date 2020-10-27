# -*- coding: utf-8 -*-
from mip.model import *

model = Model("Exemplo 3", MAXIMIZE)

# definindo as variáveis
x1 = model.add_var()
x2 = model.add_var()

# definindo a função objetivo
model += 5*x1 + 2*x2

# definindo as restrições
model += 2*x1 + 1*x2 <= 6
#model += 10*x1 + 12*x2 <= 60
model += (1/6)*x1 + (1/5)*x2 <= 8

# resolvendo o modelo
model.optimize()

#imprimindo a solução
print("x1 = {x1.x}, x2 = {x2.x}".format(**locals()))
print("custo:{}".format(model.objective_value))


