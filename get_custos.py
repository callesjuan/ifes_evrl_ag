import os, sys

nomedir = sys.argv[1]

for nomearq in os.listdir(nomedir):
  nomearq = nomedir + "/" + nomearq
  arq = open(nomearq)
  
  #linha = arq.readlines()[548]
  #print linha.split(" ")[1],
  
  for linha in arq.readlines():
    tokens = linha.split(" ")
    if tokens[0] == "custo":
      print tokens[1],
