#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime, getopt, networkx as nx, sys, traceback

def proc_entradas(layout_filename, linhas_filename, demanda_filename, bloq_filename):

  ''' ESTRUTURAS DE DADOS '''
  layout_graph = nx.DiGraph()
  bloqueios_arr = {}
  demanda_arr = []
        
  ''' LENDO ARQUIVO DE LINHAS '''
  linhas_file = open(linhas_filename, 'r')

  idx = 0
  for line in linhas_file:
    if line[0] == "#":
      continue
    tokens = line.replace("\n", "").split(" ")
    
    layout_graph.add_node(tokens[0], custo=float(tokens[1]), idx=idx)
    idx = idx + 1
    # nx.set_node_attributes(layout_graph, 'custo', {tokens[0]:tokens[1]})
  
  ''' LENDO ARQUIVO DE LAYOUT '''
  layout_file = open(layout_filename, 'r')
  
  for line in layout_file:
    if line[0] == "#":
      continue
    tokens = line.replace("\n", "").split(" ")
    src_label = tokens[0]
    edges_list = tokens[1:]

    for i in range(0, len(edges_list)/2):
      dst_label = edges_list[i*2]
      edge_custo = float(edges_list[i*2+1])
      edge_weight = layout_graph.node[src_label]['custo']/2 + edge_custo + layout_graph.node[dst_label]['custo']/2
      layout_graph.add_edge(src_label, dst_label, custo=edge_custo, weight=edge_weight)
      
  ''' LENDO ARQUIVO DE BLOQUEIOS '''
  bloq_file = open(bloq_filename, 'r')
  
  for line in bloq_file:
    if line[0] == "#":
      continue
    tokens = line.replace("\n", "").split(" ")
    
    chave = str(tokens[0]) + ", " + str(tokens[1])
    bloq_entries = []
    
    for i in range(1, len(tokens)/2):
      bloq_entries.append([str(tokens[i*2]), str(tokens[i*2+1])])
      
    bloqueios_arr[chave] = bloq_entries
      
  ''' LENDO ARQUIVO DE DEMANDA '''
  demanda_file = open(demanda_filename, 'r')
  
  for line in demanda_file:
    if line[0] == "#":
      continue
    tokens = line.replace("\n", "").split(" ")
    
    lote = [tokens[0], float(tokens[1]), float(tokens[2]), tokens[3], tokens[4]]
    
    demanda_arr.append(lote)
    
  return (layout_graph, bloqueios_arr, demanda_arr)
