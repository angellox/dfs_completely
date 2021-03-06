# -*- coding: utf-8 -*-
__author__ = 'Ángel Cruz'

import ast, resource,operator, sys
from scipy.spatial import distance
from collections import defaultdict

sys.setrecursionlimit(10 ** 6)
#GLOBALS
leaf = []
children = defaultdict(list)
#FUNCTION DOES THE READING OF THE FILE.
def readFile(archivo):
  f = open(archivo)
  return f.readlines()

def createGraph(preGraph, Graph):
  current = [ 0, (0, 0) ] #[NODE'S ID, (X,Y)]
  while current[0] != len(preGraph):
    neighbors = []
    #preNeighbors={}                                                                    #LINEA agregada PARA EVALUAR POR DISTANCIA
    current = preGraph.pop(0) #NODE'S ID
    Graph[current[0]] = neighbors
    for element in preGraph:
      if distance.euclidean(current[1], element[1]) < 100:
        #preNeighbors[element[0]]=distance.euclidean(current[1], element[1])              #LINEA agregada PARA EVALUAR POR DITANCIA
        neighbors.append( element[0] )                                                    #se debe comentar para evaluar por ditancia
        neighbors.sort(reverse =  False) #FALSE BY MIN, AND TRUE BY MAX.                   #se debe comentar para evaluar por ditancia
    #vecinos_sort = sorted(preNeighbors.items(), key=operator.itemgetter(1), reverse=False) #true-by max, false-by min    LINEA agregada PARA EVALUAR POR DITANCIA
    #for vecinitos in vecinos_sort:                                                         #LINEA agregada PARA EVALUAR POR DITANCIA
      #neighbors.append(int(vecinitos[0]))                                                  #LINEA agregada PARA EVALUAR POR DITANCIA

    preGraph.append(current)
  
  return Graph


#stack [2,4]   |    visited [1,3,5,6,4,2]    |    current = 4
def dfs(Graph_Ready, visited, n):
  global leaf, children
  flag = 1
  Graph = Graph_Ready
  neighborsList = list(Graph_Ready.values())
  visited.add(n)

  print(n, end='-> ')

  for neighbour in neighborsList[n - 1]: #[2,3]
    if neighbour not in visited:
      children[n].append(neighbour)
      flag = 0
      dfs( Graph, visited, neighbour )

  if ( flag == 1 ):
    leaf.append(n)
    print("\n")

def FindMaxChildren(children):
  nodes_deadheat = [] # ALMACENA A LOS NODOS QUE ENCUENTRA EN CASO DE EMPATE.
  key_list = list(children.keys()) #NODES
  lst = list(children.values()) #NEIGHBOURS
  maxList = max(lst, key = len)
  #print(len(maxList))
  for element in lst:
    if len(maxList) == len(element):
      position = lst.index(element)
      node = key_list[position]
      nodes_deadheat.append(node)
      print('Node: ', node, '| Numbers of children: ', len(maxList), '| Children: ', element)

  #print(nodes_deadheat)
  if nodes_deadheat: #EN CASO DE EMPATE.
    node_max = max(nodes_deadheat) #IMPRIMIMOS NODO MÁXIMO.
    node_min = min(nodes_deadheat) #IMPRIMIMOS NODO MÍN.
    print('\nNode Max: ', node_max, '| Node Min: ', node_min)
  else:
    print('Node: ', key_list[lst.index(maxList)] , '| Numbers of children: ', len(maxList), '| Children: ', maxList)


def amountOfNodes(children):
  nodes_amount = [] # ALMACENA A LOS NODOS QUE TIENEN MÁS DE 1 HIJO.
  key_list = list(children.keys()) #NODES
  lst = list(children.values()) #NEIGHBOURS

  for element in lst:
    if len(element) >= 2:
      position = lst.index(element)
      node = key_list[position]
      nodes_amount.append(node)

  print("Amount of nodes with more than 1 child: ", len(nodes_amount))

if __name__ == '__main__':
  file_ready = readFile('Network11.txt')
  preGraph = []
  Graph = {}
  visited = set()

  for line in file_ready:
    idNode = int(line.split(":")[0]) #BY OBTAINING NODE'S ID.
    coordinates = ast.literal_eval(line.split(":")[1].rstrip()) #BY OBTAINING NODE'S ID.
    items = [idNode, coordinates]
    preGraph.append(items)

  Graph_Ready = createGraph(preGraph, Graph)
  print("Graph Created: ",Graph_Ready, "\n")
  print("---THE ROUTE GETS BY DFS IS: ---\n")
  dfs(Graph_Ready, visited, 291) #(graph, visited, root_to_start)
  print("\n----------------------------------------------\n")
  print("Container Leaves: ", leaf)
  print("Leaves' Number: ", len( leaf ))
  print("\n")
  print('Nodes with their children: ' + str(dict(children)))
  print("\n")
  FindMaxChildren(children)
  amountOfNodes(children)
