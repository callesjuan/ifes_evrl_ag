#!/usr/bin/env python
# -*- coding: utf-8 -*-

import networkx as nx
from random import*
from itertools import islice
import entradas

def k_shortest_paths(G, source, target, k, weight=None):
  return list(islice(nx.shortest_simple_paths(G, source, target, weight=weight), k))

def printGeracao(lstGeracao):
  for i in range(len(lstGeracao)):
    cromossomo = lstGeracao[i]
    for gene in cromossomo:
      print(gene)
    print() 
    
def minCustoVirador(Graph,linhaOrigem,lstVirador): # retorna o virador com menor custo
  lstMinCusto = []
  lstArestas = []

  menor_custo = float("Inf")
  menor_virador = lstVirador[0]
  
  for virador in lstVirador:
    custo = nx.shortest_path_length(Graph,linhaOrigem,virador,weight = "weight")
    if custo < menor_custo:
      menor_custo = custo
      menor_virador = virador
      
  return menor_virador
  
  
def AumentaCustoVirador(Graph,virador): # aumenta o custo de um virador
  
  lstArestas = list(Graph.predecessors(virador))
  for i in range(len(lstArestas)):
    custoAtual = Graph[lstArestas[i]][virador]["weight"]
    # custoAdicional = randint(0,Graph.graph['delta_lotes']) # aleatorio
    custoAdicional = Graph.graph['delta_lotes']
    Graph[lstArestas[i]][virador]["weight"] += custoAdicional
    
def AumentaCustoRota(Graph,rota): # aumenta o custo de um virador
  
  anterior = None
  for linha in rota:
    if anterior is not None:
      #custoAdicional = Graph.edge[anterior][linha]['weight']/2
      custoAdicional = uniform(0,Graph.edge[anterior][linha]['weight'])
      Graph.edge[anterior][linha]['weight'] += custoAdicional
    anterior = linha


# cria uma geração de cromossomos de maneira aleatória, escolhe o virador de maneira aletória 

def si_aleatoria(G,demanda,qtdCromossomos):
  
  qtdLotes = len(demanda)
  lstGene = []
  lstCromossomo = []
  lstGeracao = []
  
  for i in range(qtdCromossomos):
    for j in range(qtdLotes):
      linhaOrigem = demanda[j][3]
      
      if demanda[j][4] == 'F':
        lstDestino = G.graph['linhas_formacao']
      elif demanda[j][4] == 'M':
        lstDestino = G.graph['pial']
      else:
        lstDestino = G.graph['viradores']
      
      pos = randint(0,len(lstDestino)-1)
      virador = lstDestino[pos]
      # lstGene = nx.shortest_path(G,linhaOrigem,virador,weight = "weight")
      
      k = 6
      candidatos = k_shortest_paths(G, linhaOrigem, virador, k, weight="weight")
      if len(candidatos) < k:
        k = len(candidatos)
      pos_candidato = randint(0, k-1)
      lstGene = candidatos[pos_candidato]
      
      lstCromossomo.append(lstGene)
    lstGeracao.append(lstCromossomo)
    lstCromossomo = []
  
  return lstGeracao

# cria uma geração de cromossomos de maneira deterministica, escolhe sempre o virador com menor custo
  
def si_deterministica(Grafo,demanda,qtdCromossomos): 
  
  qtdLotes = len(demanda)
  lstGene = []
  lstCromossomo = []
  lstGeracao = []
  
  for i in range(qtdCromossomos):
    gcopy = Grafo.copy()
    for j in range(qtdLotes):
      linhaOrigem = demanda[j][3]
      
      if demanda[j][4] == 'F':
        lstDestino = G.graph['linhas_formacao']
      elif demanda[j][4] == 'M':
        lstDestino = G.graph['pial']
      else:
        lstDestino = G.graph['viradores']
    
      virador = minCustoVirador(gcopy,linhaOrigem,lstDestino)
      lstGene = nx.shortest_path(gcopy,linhaOrigem,virador,weight = "weight")
      lstCromossomo.append(lstGene)
      AumentaCustoRota(gcopy,lstGene)
    lstGeracao.append(lstCromossomo)
    lstCromossomo = []
  
  return lstGeracao  
        

def main():
  
  layout, bloqueio, lstDemanda= entradas.proc_entradas("entradas/wlayout", "entradas/linhas", "entradas/demanda", "entradas/bloqueios")
  
  layout.graph['linha_origem'] = '1A1'
  layout.graph['viradores'] = ['VV01T', 'VV02T', 'VV03T', 'VV04T', 'VV05T', 'VV06T']
  layout.graph['delta_lotes'] = 375.0
  
  
  
  printGeracao(SolucInicAleatorio(layout,lstDemanda,4))
  print("--------------------------------------------------")
  printGeracao(SolucInicDetertministica(layout,lstDemanda,4))
  
  
  return 0

#main()
