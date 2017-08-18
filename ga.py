#!/usr/bin/env python
# -*- coding: utf-8 -*-

import networkx as nx
import operator
import crossover
import mutation
import solucaoinicial as si
import time
import simulacao

solucaoinicial_func = si.si_aleatoria # solucao inicial (aleatória ou determinística)
fitness_func = simulacao.fitness
mutacao_func = mutation.mutation3

repeated = 0.3

#falta receber os outros parâmetros da fitness (ex: bloqueios, demanda)
def ga(G1, bloqueios1, demanda1, iterations1, mutationProbability1, selectoinHardness1):
  
  global G
  global bloqueios
  global demanda
  global mutationProbability
  global iterations
  global selectoinHardness
  global generation

  global best
  global repeated
  
  G = G1
  bloqueios = bloqueios1
  demanda = demanda1
  mutationProbability = mutationProbability1
  iterations = iterations1
  selectoinHardness = selectoinHardness1
  generation = solucaoinicial_func(G, demanda, selectoinHardness)
  prepare()
  best = generation[0]
  
  repeated = round(repeated * selectoinHardness, 0)
  
  start()
  return (fitness_func(generation[0], G, bloqueios, demanda), generation[0], fitness_func(best, G, bloqueios, demanda), best)


def start():

  global iterations
  
  global G
  global bloqueios
  global demanda
  global generation
  global best
  
  for count in range(0, iterations):
    lens = []
    lens.append(len(generation))
    
    cross()
    lens.append(len(generation))
    
    # prepare()
    
    mutate()
    lens.append(len(generation))
    
    # prepare()
    prepare_adaptativo()
       
    seleciona()


def cross():
  
  start = time.clock()
  
  global generation
  generation = crossover.crossover2(generation)
  
  elapsed = time.clock()
  elapsed = elapsed - start
  # print 'cross' , elapsed
  
def prepare():
  global generation

  #cria um lista de containers, que será usada para ordenar os cromossomos em função do tempo
  #de cada cromossomo
  chromosomeContainerList = []
  
  #tira de 'generation' e joga pro container
  for i in range(len(generation)):
    chromosomeContainerList.append((fitness_func(generation[i], G, bloqueios, demanda)[1], generation[i]))
  
  #Ordena
  chromosomeContainerList = sorted(chromosomeContainerList, key = operator.itemgetter(0))
  
  generation = []
  
  #tira do container e coloca de volta em 'generation'
  for i in range(len(chromosomeContainerList)):
    generation.append(chromosomeContainerList[i][1])
  
def prepare_adaptativo():
  global generation
  
  global G
  global bloqueios
  global demanda
  global mutationProbability

  #cria um lista de containers, que será usada para ordenar os cromossomos em função do tempo
  #de cada cromossomo
  chromosomeContainerList = []
  
  dic = {}
  
  #tira de 'generation' e joga pro container
  for i in range(len(generation)):
    custo_gen = fitness_func(generation[i], G, bloqueios, demanda)
    if dic.has_key(custo_gen[1]):
      dic[custo_gen[1]].append((custo_gen[1], generation[i]))
    else:
      dic[custo_gen[1]] = [(custo_gen[1], generation[i])]
      
  for chave in dic:
    if len(dic[chave]) >= repeated:
      chromosomeContainerList.append(dic[chave].pop(0))
      aux = []
      while len(dic[chave]) > 0:
        sol = dic[chave].pop()
        mutado = mutacao_func(G, sol[1], 50)
        nova_sol = (fitness_func(mutado[0], G, bloqueios, demanda), mutado[0])
        aux.append(nova_sol)
      chromosomeContainerList.extend(aux)
    else:
      chromosomeContainerList.extend(dic[chave])
  
  #Ordena
  chromosomeContainerList = sorted(chromosomeContainerList, key = operator.itemgetter(0))
  
  generation = []
  
  #tira do container e coloca de volta em 'generation'
  for i in range(len(chromosomeContainerList)):
    generation.append(chromosomeContainerList[i][1])
  

def mutate():
  
  start = time.clock()
  
  global G
  global generation
  global mutationProbability
  
  for i in range(len(generation)):
    mutante, mutou = mutacao_func(G, generation[i], mutationProbability)
    if mutou:
      generation.append(mutante)
      generation[i] = mutante
    
  elapsed = time.clock()
  elapsed = elapsed - start
  # print 'mutate' , elapsed


def seleciona():

  start = time.clock()
  
  global G
  global bloqueios
  global demanda
  global mutationProbability
  global iterations
  global selectoinHardness
  global generation
  global best
  
  #elimina as piores soluçoes que estrapolam o limite máximo de uma geração
  if(len(generation) > selectoinHardness):
    generation = generation[0:selectoinHardness]
    
  elapsed = time.clock()
  elapsed = elapsed - start
  # print 'seleciona' , elapsed
  
  best_fitness = fitness_func(best, G, bloqueios, demanda)
  generation_fitness = fitness_func(generation[0], G, bloqueios, demanda)
  
  if generation_fitness[1] < best_fitness[1]:
    best = generation[0]
    







