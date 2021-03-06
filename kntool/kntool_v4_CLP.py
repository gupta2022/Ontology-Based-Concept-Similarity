import nltk
import spacy
import re
import pandas as pd
#import bs4
#import requests
#from spacy import displacy
#from nltk.tokenize import sent_tokenize
#nlp = spacy.load('en_core_web_sm')
#from spacy.matcher import Matcher
from spacy.tokens import Span
import networkx as nx
import matplotlib.pyplot as plt
from tqdm import tqdm
from nltk.tokenize import PunktSentenceTokenizer
pst = PunktSentenceTokenizer()
openfile = open("data.txt")
data = openfile.read()
data =re.sub('\. ','.',data)
data =re.sub('\).','\) .',data)

print (data)
tokenized_sentence = pst.tokenize(data)
stringlist = []
for i in tokenized_sentence:
  try:
    words = nltk.word_tokenize(i)
    tagged = nltk.pos_tag(words)
    chunkGram = r"""Chunk: {<JJ.?>*<NN.?>+<NN..?>*}"""
    chunkParser = nltk.RegexpParser(chunkGram)
    chunked = chunkParser.parse(tagged)
    print(chunked)
    stringlist.append(chunked.pformat().encode('ascii','ignore'))
  except Exception as e:
      print(str(e))
#print(len(stringlist[1]))
#String = stringlist[1]
index = 0
listoflist = []
for f in stringlist:
 String = f
 #print(len(String))
 chunklist = []
 iter = re.finditer(r"\Chunk\b", String)
 indices = [m.start(0) for m in iter]
 #print(indices)
 for x in indices:
#print(stringlist[1][x+5])#space
#get the word from space till /
#print(x)
  j=1
  temp =""
  while(stringlist[index][x+5+j]!=')'):
   temp = temp + stringlist[index][x+5+j]
   j = j+1
 # print(temp)
  chunklist.append(temp)
 index = index + 1
 listoflist.append(chunklist)
print(listoflist)
#make a source list and make a target list
#first n-1 in a list are source and last n-1 are in the target list
#add them to pandas data frame
#form the graph
source = []
target = []
for i in listoflist:
 temp_source = []
 temp_target = []
 for j in i:
   temp_source.append(j)
   temp_target.append(j)
 if len(temp_source)!=0 and len(temp_target)!=0:
  temp_source.pop(len(temp_source)-1)
  temp_target.pop(0)
 for x in temp_source:
     source.append(x)
 for y in temp_target:
     target.append(y)
print(source)#already formed the source list
print(target)#target list formed
kg_df = pd.DataFrame({'source':source, 'target':target})
print("printing pandas data frame--------")
print(kg_df)
G=nx.from_pandas_edgelist(kg_df, "source", "target")
print("Performing CLP calculations")
for i in source :
  temp_sum = 0
  for j in target:
   temp_sum = temp_sum + nx.shortest_path_length(G,i,j)  
  print(i+"--->"+str(temp_sum))


plt.figure(figsize=(12,12))
pos = nx.spring_layout(G)
nx.draw(G, with_labels=True, node_color='skyblue', edge_cmap=plt.cm.Blues, pos = pos)
plt.show()
