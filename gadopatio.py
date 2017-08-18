#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime, getopt, networkx as nx, numpy as np, sys, time, traceback
import entradas, ga, simulacao

'''
ENTRADA:
  LAYOUT (NÓS E ENLACES), DEMANDA E BLOQUEIOS
SAIDA:
  CRONOGRAMA DOS LOTES (ACRESCENTANDO-LHES ROTA E TEMPO DE CHEGADA NO VIRADOR)
'''

if __name__ == '__main__':
  print "GA do Pátio..."
    
  opts, args = getopt.getopt(sys.argv[1:], "l:n:d:b", ['layout=', 'linhas=', 'demanda=', 'bloqueios='])
    
  for opt, arg in opts:
    if opt in ('-l', '--layout'):
      layout_filename = arg
    if opt in ('-n', '--linhas'):
      linhas_filename = arg
    if opt in ('-d', '--demanda'):
      demanda_filename = arg
    if opt in ('-b', '--bloqueios'):
      bloq_filename = arg
      
  layout, bloqueios, demanda = entradas.proc_entradas(layout_filename, linhas_filename, demanda_filename, bloq_filename)
  
  layout.graph['linhas_origem'] = ['L00']
  layout.graph['viradores'] = ['L30', 'L31', 'L32']
  layout.graph['linhas_formacao'] = ['L60', 'L61', 'L62']
  layout.graph['pial'] = ['L63']
  layout.graph['delta_lotes'] = 10
  
  ga_iter = 250 # numero de iteracoes
  ga_mutacao = 10 # numero de um a cem
  ga_nindividuos = 50 # numero de individuos por geracao
	
  t0 = time.clock()
  result = ga.ga(layout, bloqueios, demanda, ga_iter, ga_mutacao, ga_nindividuos)
  tf = time.clock() - t0
  
  custos = result[0]
  solucao = result[1]
  
  # IMPRESSÃO DA SOLUÇÃO FINAL
  '''
  print
  print 'executou em', tf, 'ms'
  '''
  
  # print 'custo', custos[1], 'best', result[2][1]
  print 'custo', custos[1]
  for lote, rota, custo in zip(demanda, solucao, custos[0]):
    print rota, custo
  
  # IMPRESSÃO DA SIMULAÇÃO DA SOLUÇÃO FINAL
  ts = simulacao.simulacao(solucao, layout, bloqueios, demanda)
  lote = demanda[len(demanda)-1]
  rota = solucao[len(solucao)-1]
  ts_lote = ts[lote[0]]
  makespan = ts_lote[rota[len(rota)-1]]['t_tras_saida'] - demanda[0][1]
  print 'makespan', makespan

  for lote, rota, custo in zip(demanda, solucao, custos[0]):
    ts_lote = ts[lote[0]]
    ts_print = []
    custo_real = ts_lote[rota[len(rota)-1]]['t_tras_saida'] - lote[1]
    
    print
    print lote[0], lote[1]
    print rota, custo, custo_real
    
    for linha in rota:
      ts_print_row = [ts_lote[linha]['t_frente_entrada'], ts_lote[linha]['t_frente_saida'], ts_lote[linha]['t_tras_entrada'], ts_lote[linha]['t_tras_saida']]
      ts_print.append(ts_print_row)
      
      print linha, ts_print_row, ts_lote[linha]['atraso']
      
  print
  print
  print
  
  # MANUTENÇÃO E FORMAÇÃO
  
  demanda2 = []
  
  for i in range(0, len(demanda)):
    demanda[i][4] = demanda[i][4].replace("V", "")
    
    lote = demanda[i][0]
    chegada = demanda[i][1] + custos[0][i] - layout.graph['delta_lotes']
    
    # origem = solucao[i][len(solucao[i])-1]
    origem = layout.successors(solucao[i][len(solucao[i])-1])[0]
    
    d1 = [str(lote + "-1"), chegada, layout.graph['delta_lotes']/2, origem, demanda[i][4][0]]
    d2 = [str(lote + "-2"), chegada + layout.graph['delta_lotes']/2, layout.graph['delta_lotes']/2, origem, demanda[i][4][1]]
    
    demanda2.append(d1)
    demanda2.append(d2)
    
  # print demanda2
  
  t0 = time.clock()
  result = ga.ga(layout, bloqueios, demanda2, ga_iter, ga_mutacao, ga_nindividuos)
  tf = time.clock() - t0
  
  custos = result[0]
  solucao = result[1]
  
  print 'custo', custos[1]
  for lote, rota, custo in zip(demanda2, solucao, custos[0]):
    print rota, custo
    
  # IMPRESSÃO DA SIMULAÇÃO DA SOLUÇÃO FINAL
  ts = simulacao.simulacao(solucao, layout, bloqueios, demanda2)
  lote = demanda2[len(demanda2)-1]
  rota = solucao[len(solucao)-1]
  ts_lote = ts[lote[0]]
  makespan = ts_lote[rota[len(rota)-1]]['t_tras_saida'] - demanda2[0][1]
  print 'makespan', makespan

  for lote, rota, custo in zip(demanda2, solucao, custos[0]):
    ts_lote = ts[lote[0]]
    ts_print = []
    custo_real = ts_lote[rota[len(rota)-1]]['t_tras_saida'] - lote[1]
    
    print
    print lote[0], lote[1]
    print rota, custo, custo_real
    
    for linha in rota:
      ts_print_row = [ts_lote[linha]['t_frente_entrada'], ts_lote[linha]['t_frente_saida'], ts_lote[linha]['t_tras_entrada'], ts_lote[linha]['t_tras_saida']]
      ts_print.append(ts_print_row)
      
      print linha, ts_print_row, ts_lote[linha]['atraso']
