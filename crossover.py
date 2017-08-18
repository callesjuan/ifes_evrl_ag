#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

def printGeracao(lstGeracao):
  for i in range(len(lstGeracao)):
    cromossomo = lstGeracao[i]
    for gene in cromossomo:
      print(gene)
    print() 


def printCromossomo(cromossomo):
  for gene in cromossomo:
    print(gene)
  print() 
    
    
def crossover(lstSolucao):
          
  lstFilhos = []
  lstGene1 = []
  lstGene2 = []
  lstCruzamentoGene = []

  for i in range(len(lstSolucao)-1):
    cromossomo1 = lstSolucao[i]
    
    
    for l in range(i+1,len(lstSolucao),1):
      
      cromossomo2 = lstSolucao[l]
      for j in range(len(cromossomo1)):
        if(j%2 == 0):
        
          lstGene1 = cromossomo1[j]
          lstCruzamentoGene.append(lstGene1)
        else:  
          lstGene2 = cromossomo2[j]
          lstCruzamentoGene.append(lstGene2)
            
      lstFilhos.append(lstCruzamentoGene)
      lstCruzamentoGene = []
  
  
  return lstFilhos
  
def crossover2(lstSolucao):
  lstFilhos = []

  while len(lstSolucao) > 0:
    i1 = random.randint(0,len(lstSolucao)-1)
    c1 = lstSolucao.pop(i1)
    
    if len(lstSolucao) > 0:
      i2 = random.randint(0,len(lstSolucao)-1)
      c2 = lstSolucao.pop(i2)
    
      c3 = []
      # c4 = []
      for i in range(len(c1)):
        if i % 2 == 0:
          c3.append(c1[i])
          # c4.append(c2[i])
        else:
          c3.append(c2[i])
          # c4.append(c1[i])
      
      lstFilhos.append(c1)
      lstFilhos.append(c2)
      lstFilhos.append(c3)
      # lstFilhos.append(c4)
    else:
      lstFilhos.append(c1)
      
  return lstFilhos

def main():
  
  lstSolucao = [[[1,3,8,9,10,13],  # lot1
          [1,4,6,8,12,14],   # lot2
          [1,5,7,9,15],      # lot3
          [1,4,6,8,9]],      # lot4
         
         [[1,3,5,6,8,16],
          [1,4,7,9,12],
          [1,3,5,7,10,14],
          [1,5,7,8,9]],   
         
         [[1,4,6,8,9,10],
          [1,4,6,8,9,12],
          [1,3,6,8,9],
          [1,3,5,7,8,9]],   
         
         [[1,4,6,7,9,12],
          [1,5,6,7,9],
          [1,2,5,8,9,15],
          [1,4,6,8,9,10]]]
  
  
  
  printGeracao(crossover2(lstSolucao))
  
#main()
