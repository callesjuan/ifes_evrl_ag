#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import randint
import networkx as nx



def calculaChance(percentual):
  
  if(percentual < 1): return False
  if(percentual > 100): percentual = 100
  if(randint(0, 100) <= percentual):
    return True
  else:
    return False




def encontraNoAlternativo(nodesList, listaExcluidos):
  
  ctrl = True
  
  for i in range(0, 5):
    intRand = randint(0, len(nodesList) - 1)
    no = nodesList[intRand]
    for j in range(len(listaExcluidos)):
      if(no == listaExcluidos[j]):
        ctrl = False
        break
    if(ctrl): return intRand
    ctrl = True
  return -1



def mutation(G, chromosome, percentual):
  
  #nodesList = nx.nodes(G)
  nodesList = list(G.nodes())
  
  for i in range(len(chromosome)):
    if(len(chromosome[i]) > 1):
      
      #verifica se vai ou não sofrer mutação baseado na porcentagem armazenada em 'percentual' 
      if(calculaChance(percentual) == True):
        
        #escole um nó da rota, que não seja o ultimo
        no1Index = randint(0, len(chromosome[i]) - 2)
        
        #tenta encontrar um nó que não seja igual a nenhum dos nos da lista 'listaExcluidos'
        no2Index = encontraNoAlternativo(nodesList, [chromosome[i][no1Index]])
        
        #Se a função 'encontraNoAlternativo()' não encontrou nenhum nó possível, 'no2Index'
        #será igual a -1 e o programa não entrará no if.
        #Do contrário 'no2Index' será maior que -1, o que significa que existe um nó possivel
        #de ser utilizado, então o prgrama entrará no if.
        if(no2Index > -1): 
          try:
            
            #gera a menor rota do nó1 até o nó2 e depois do nó2 até o nó3, sendo que o
            #nó3 é o nó que está a frente do nó um na sequencia da rota em questão 
            rotaNo1No2 = nx.dijkstra_path(G, chromosome[i][no1Index], nodesList[no2Index])
            rotaNo2No3 = nx.dijkstra_path(G, nodesList[no2Index], chromosome[i][no1Index + 1])
            
            #juta-se a parte inicial da rota em questão com as novas
            #rotas, rotaNo1No2 e rotaNo2No3.
            #A nova rota que é criada, ira substituir a rota que estava sendo
            #analisada, concluindo a mutação
            rota = chromosome[i][0:no1Index] + rotaNo1No2[0:len(rotaNo1No2) - 1] + rotaNo2No3
            chromosome[i] = rota
          except nx.NetworkXNoPath as e:
            
            #Se o algoritmo do DJ-Kastra não conseguir criar a rota 'rotaNo1No2'
            #ou a 'rotaNo2No3', nada deve acontecer. A rota que está sendo analisada não
            #sofrerá nenhuma alteração (não sofrerá mutação)
            
            #Estou alterando o valor da variavel 'no1Index' para zero porque se a seção
            #do 'except' ficar vazia o Python enche o saco.
            no1Index = 0
  return chromosome
  

def mutation2(G, chromosome, percentual):
  
  #nodesList = nx.nodes(G)
  nodesList = list(G.nodes())
  
  for i in range(len(chromosome)):
    if(len(chromosome[i]) > 1):
      
      #verifica se vai ou não sofrer mutação baseado na porcentagem armazenada em 'percentual' 
      if(calculaChance(percentual) == True):
        
        #escole um nó da rota, que não seja o ultimo
        no1Index = randint(0, len(chromosome[i]) - 2)
        
        #tenta encontrar um nó que não seja igual a nenhum dos nos da lista 'listaExcluidos'
        no2Index = encontraNoAlternativo(nodesList, [chromosome[i][no1Index]])
        
        #Se a função 'encontraNoAlternativo()' não encontrou nenhum nó possível, 'no2Index'
        #será igual a -1 e o programa não entrará no if.
        #Do contrário 'no2Index' será maior que -1, o que significa que existe um nó possivel
        #de ser utilizado, então o prgrama entrará no if.
        if(no2Index > -1): 
          try:
            
            #gera a menor rota do nó1 até o nó2 e depois do nó2 até o nó3, sendo que o
            #nó3 é o nó que está a frente do nó um na sequencia da rota em questão 
            rotaNo1No2 = nx.dijkstra_path(G, chromosome[i][no1Index], nodesList[no2Index])
            rotaNo2No3 = nx.dijkstra_path(G, nodesList[no2Index], chromosome[i][no1Index + 1])
            
            #juta-se a parte inicial da rota em questão com as novas
            #rotas, rotaNo1No2 e rotaNo2No3.
            #A nova rota que é criada, ira substituir a rota que estava sendo
            #analisada, concluindo a mutação
            rota = chromosome[i][0:no1Index] + rotaNo1No2[0:len(rotaNo1No2) - 1] + rotaNo2No3
            print()
            print chromosome[i]
            print no1Index, no2Index
            print rotaNo1No2
            print rotaNo2No3
            print rota
            print()
            asd = input()
            chromosome[i] = rota
          except nx.NetworkXNoPath as e:
            
            #Se o algoritmo do DJ-Kastra não conseguir criar a rota 'rotaNo1No2'
            #ou a 'rotaNo2No3', nada deve acontecer. A rota que está sendo analisada não
            #sofrerá nenhuma alteração (não sofrerá mutação)
            
            #Estou alterando o valor da variavel 'no1Index' para zero porque se a seção
            #do 'except' ficar vazia o Python enche o saco.
            no1Index = 0
  return chromosome
  
  
def mutation3(G, chromosome, percentual):
  
  #nodesList = nx.nodes(G)
  nodesList = list(G.nodes())
  
  mutou = False
  
  if(calculaChance(percentual) == False):
    return [chromosome, mutou]
  
  for i in range(len(chromosome)):
    if(len(chromosome[i]) > 1):
      
      #verifica se vai ou não sofrer mutação baseado na porcentagem armazenada em 'percentual' 
      if(calculaChance(percentual) == True):
      
        mutou = True
        
        if chromosome[i][len(chromosome[i])-1] in G.graph['viradores']:
          lstDestino = G.graph['viradores']
        elif chromosome[i][len(chromosome[i])-1] in G.graph['linhas_formacao']:
          lstDestino = G.graph['linhas_formacao']
        else:
          lstDestino = G.graph['pial']
                  
        #escole um nó da rota, que não seja o ultimo
        no1Index = randint(0, len(chromosome[i]) - 2)
        no2Index = randint(0, len(lstDestino) - 1)
        no_sorteado = chromosome[i][no1Index]
        destino = lstDestino[no2Index]
        
        try:
          rota = nx.dijkstra_path(G, no_sorteado, destino)
          chromosome[i] = chromosome[i][0:no1Index] + rota
        except nx.NetworkXNoPath as e:
          pass
  return (chromosome, mutou)
