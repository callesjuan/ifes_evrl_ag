#!/usr/bin/env python
# -*- coding: utf-8 -*-

import collections, datetime, getopt, math, networkx as nx, sys, traceback

def getOverlap(a, b):
  return max(0, min(a[1], b[1]) - max(a[0], b[0]))
    
def vias_ocupadas(lote, rota, via, layout):
  '''
  retorna as vias (linhas e enlaces) que um lote está usando num determinado instante/tempo t
  '''  
  vias_arr = []
  ts_arr = []
  
  t = 0
  anterior = None
  for linha2 in rota:
    if anterior is not None:
      t += layout.edge[anterior][linha2]['custo']
      enlace = str(anterior + ", " + linha2)
      vias_arr.append(enlace)
      ts_arr.append(t)
      
      if via == enlace:
        break
      
    t += layout.node[linha2]['custo']
    vias_arr.append(linha2)
    ts_arr.append(t)
    
    if via == linha2:
      break
      
    anterior = linha2
      
  t_corte = t - layout.graph['delta_lotes'] if (t - layout.graph['delta_lotes']) >= 0 else 0
  
  vias = []
  
  t = 0
  anterior = None
  for linha2 in rota:
    if anterior is not None:
      t += layout.edge[anterior][linha2]['custo']
      
      if t >= t_corte:
        enlace = str(anterior + ", " + linha2)
        vias.append(enlace)        
      
    t += layout.node[linha2]['custo']
    if t >= t_corte:
      vias.append(linha2)
    
    if via == linha2:
      break
      
    anterior = linha2
    
  if len(vias) > 0:
    vias.pop()
  
  return vias
    
def simulacao_core(solucao, layout, bloqueios, demanda):
  
  '''
  obter os tempos em que cada lote passa em cada linha de sua rota
  em outras palavras, para cada linha de rota de um lote, obter:
    - tempo em que a ponta da frente toca no extremo inicial da linha
    - tempo em que a ponta da frente toca no extremo final da linha
    - tempo em que a ponta de trás toca no extremo inicial da linha
    - tempo em que a ponta de trás toca no extremo final da linha
    
  estratégia:
    - determinar primeiro os tempos em que a frente do lote avança
    - determinar os tempos em que a ponta de trás do lote avança, de acordo com os tempos da frente
  '''
  
  ts_via = {}
  
  for linha in layout.nodes():
    ts_via[linha] = []
  for enlace in layout.edges():
    str_enlace = str(enlace[0] + ", " + enlace[1])
    ts_via[str_enlace] = []
  
  ts_lote = {}
  tempos = []
  
  for lote in demanda:
    ts_lote[lote[0]] = {}
  
  for lote, rota in zip(demanda, solucao):
  
    lote_id = lote[0]
    t = lote[1]
    atraso_via = {}
    
    anterior = None
    
    '''
    determinando os tempos de entrada e saida referentes à parte da frente do lote
    '''   
    for linha in rota:
      ts_lote[lote_id][linha] = {}
    
      '''
      posso avançar no enlace? há outros enlaces que me bloqueiam no mesmo instante?
      '''
      if anterior is not None:
        str_enlace = str(anterior + ", " + linha)
        
        '''
        outro enlace me bloqueia?
        '''
        if bloqueios.has_key(str_enlace):
          t_atraso_bloqueio = 0
          
          for bloqueante in bloqueios[str_enlace]:
            str_bloqueante = str(bloqueante[0] + ", " + bloqueante[1])
            if len(ts_via[str_bloqueante]) > 0 and ts_via[str_bloqueante][len(ts_via[str_bloqueante])-1]['t_saida'] > t:
              atraso_via[str_enlace] = ts_via[str_bloqueante][len(ts_via[str_bloqueante])-1]['t_saida'] - t
              t_atraso_bloqueio = ts_via[str_bloqueante][len(ts_via[str_bloqueante])-1]['t_saida'] - t
          
          if t_atraso_bloqueio > 0:
            vias_atraso_bloqueio = vias_ocupadas(lote, rota, linha, layout)
            for via in vias_atraso_bloqueio:
              if atraso_via.has_key(via):
                atraso_via[via] += t_atraso_bloqueio
              else:
                atraso_via[via] = t_atraso_bloqueio
              
          t += t_atraso_bloqueio
        
        '''
        o enlace está ocupado?
        '''
        if layout.edge[anterior][linha]['custo'] > 0:
          if len(ts_via[str_enlace]) > 0 and ts_via[str_enlace][len(ts_via[str_enlace])-1]['t_saida'] > t:
            t += ts_via[str_enlace][len(ts_via[str_enlace])-1]['t_saida'] - t
              
        t += layout.edge[anterior][linha]['custo']
        
        
      '''
      posso avançar para a próxima linha? há outro lote ocupando a linha no mesmo instante?
      '''
      if len(ts_via[linha]) > 0 and ts_via[linha][len(ts_via[linha])-1]['t_saida'] > t and ts_via[linha][len(ts_via[linha])-1]['lote'] != lote_id.split('-')[0]:
        t_atraso_linha = ts_via[linha][len(ts_via[linha])-1]['t_saida'] - t
        
        if t_atraso_linha > 0:
          vias_atraso_linha = vias_ocupadas(lote, rota, linha, layout)
          for via in vias_atraso_linha:
            if atraso_via.has_key(via):
              atraso_via[via] += t_atraso_linha
            else:
              atraso_via[via] = t_atraso_linha
        
          t += t_atraso_linha
        
      ts_lote[lote_id][linha]['t_frente_entrada'] = t
      ts_lote[lote_id][linha]['t_frente_saida'] = t = t + layout.node[linha]['custo']
        
      anterior = linha
      
    '''
    falta determinar os tempos de entrada e saída da parte traseira de cada lote (ts_lote),
    além dos intervalos de ocupação das linhas e enlaces (ts_via)
    '''
    t = lote[1]
    anterior = None
    for linha in rota:
      
      ts_lote[lote_id][linha]['t_tras_entrada'] = ts_lote[lote_id][linha]['t_frente_entrada'] + layout.graph['delta_lotes']
      if atraso_via.has_key(linha):
        ts_lote[lote_id][linha]['t_tras_entrada'] += atraso_via[linha]
      ts_lote[lote_id][linha]['t_tras_saida'] = ts_lote[lote_id][linha]['t_tras_entrada'] + layout.node[linha]['custo']
      
      ts_via[linha].append({'t_entrada':ts_lote[lote_id][linha]['t_frente_entrada'], 't_saida':ts_lote[lote_id][linha]['t_tras_saida'], 'lote':lote_id.split('-')[0]})
      
      if atraso_via.has_key(linha):
        atraso = atraso_via[linha]
      else:
        atraso = 0
      ts_lote[lote_id][linha]['atraso'] = atraso
      
      if anterior is not None and layout.edge[anterior][linha]['custo'] > 0:
        enlace = str(anterior + ", " + linha)
        
        ts_via[enlace].append({'t_entrada':ts_lote[lote_id][anterior]['t_frente_saida'], 't_saida':ts_lote[lote_id][linha]['t_tras_entrada'], 'lote':lote_id.split('-')[0]})
        
    tempos.append(ts_lote[lote_id][rota[len(rota)-1]]['t_tras_saida'] - lote[1])
    
  return tempos, sum(tempos), ts_lote

def fitness(solucao, layout, bloqueios, demanda):
  result = simulacao_core(solucao, layout, bloqueios, demanda)
  return result[:2]
  
def simulacao(solucao, layout, bloqueios, demanda):
  result = simulacao_core(solucao, layout, bloqueios, demanda)
  return result[2]
  
  
