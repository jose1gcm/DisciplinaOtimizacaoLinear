# -*- coding: utf-8 -*-
from mip.model import *
model = Model()
model.read('pharmacy.lp')
model.optimize()
print("Solução ótima com custo: {}\n".format(model.objective_value))
