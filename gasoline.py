# -*- coding: utf-8 -*-
"""
Created on Sun Feb  3 18:13:21 2019

@author: Yaya Liu
"""

from gurobipy import *

Ingredients = ('Gas1', 'Gas2', 'Gas3', 'Gas4')
Composition = ('Index1', 'Index2')

Percentcomp = {
        ('Gas1', 'Index1'):99,
        ('Gas1', 'Index2'):210,
        ('Gas2', 'Index1'):70,
        ('Gas2', 'Index2'): 335,
        ('Gas3', 'Index1'): 78,
        ('Gas3', 'Index2'): 280,
        ('Gas4', 'Index1'): 91,
        ('Gas4', 'Index2'): 265
        }


Cost = {
        'Gas1': 48,
        'Gas2': 43,
        'Gas3': 58,
        'Gas4': 46
        }

MaxBlend = {
        'Index1': 90,
        'Index2': 280
        }

MinBlend = {
        'Index1': 85,
        'Index2': 270
        }

gas = Model()

gas.modelSense = GRB.MINIMIZE

gas.update()

mix = {}

for ing in Ingredients:
    mix[ing] = gas.addVar(vtype = GRB.CONTINUOUS,
                           obj = Cost[ing],
                           lb = 0,
                           name = 'ing'
            )

gas.update()


gasConstraints = {}
constrName = 'Least'
gasConstraints[constrName] = gas.addConstr(quicksum(mix[i] for i in Ingredients)
                                             == 1,
                                            name = constrName)
gas.update()  

for comp in Composition:
    constrName = 'MaxBlend' + comp
    gasConstraints[constrName] = gas.addConstr(quicksum(mix[i]*Percentcomp[i,comp] for i in Ingredients)
                                  <= MaxBlend[comp] * quicksum(mix[i] for i in Ingredients),
                                  name = constrName)
    
gas.update()   


for comp in Composition:
    constrName = 'MinBlend' + comp
    gasConstraints[constrName] = gas.addConstr(quicksum(mix[i]*Percentcomp[i,comp] for i in Ingredients)
                                  >= MinBlend[comp] * quicksum(mix[i] for i in Ingredients),
                                  name = constrName)
    
gas.update()  

gas.write('gas.lp')
gas.optimize()
gas.write('gas.sol')


for m in mix:
    if mix[m].x > 0:
        print(m, round(mix[m].x,2))
