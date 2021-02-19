import fileinput
from typing import Type


def get_file_data(input):
    links = {}
    for line in input:
        line = line.rstrip("\n").split(",")
        if(line[0]==''):
            nodes = line[1:]
        else:
            temp = {nodes[i]:int(line[1:][i]) for i in range(len(nodes))}
            links.update({line[0]:temp})
    return nodes,links




class Distace_Vector(object):
    class Node:
        def __init__(self,name,vertices) -> None:
            self.name = name
            self.verts = vertices

        def check(self,Dv,c):
            for i in self.verts:
                if( Dv[i]+c < self.verts[i]):
                    self.verts[i]=Dv[i]+c

        def __getitem__(self,other):
            return self.verts[other]

        def __iter__(self):
            return self.verts.__iter__()

        def __setitem__(self,key,value):
            self.verts[key] = value

        def __add__(self,value):
            return {i:self.verts[i]+value for i in self.verts}

        def __repr__(self) -> str:
            return repr(self.verts)

    def __init__(self,nodes,links) -> None:
        self.nodes = nodes
        self.graph = {i:self.Node(i,links[i]) for i in nodes}
        

    def bellman_ford(self):
        for _ in range(len(self.nodes)-1):
            for u in self.nodes:
                for v in self.nodes:
                    self.graph[u].check(self.graph[v],self.cost(u,v))

    def cost(self,u,v):
        return self.graph[u][v]

    def __getitem__(self,other):
        return self.graph[other]

    def __setitem__(self,key,value):
        self.graph[key] = value

    def __str__(self) -> str:
        table=""
        for i in self.graph:
            values = ' '.join([str(self.graph[i][a]) for a in self.graph[i]])
            table+=f"Distance vector for node {i}: {values}\n"
        return table


class Dijkstras:

    class Node:
        def __init__(self,val) -> None:
            self.val = val
            self.prev = ""
            self.tree = ""
        
        def __repr__(self) -> str:
            return repr({'val':self.val,'prev':''})

    def __init__(self,nodes,links,start_node) -> None:
        self.unvisited = nodes
        self.start = start_node
        self.links = links
        self.distances = {i:self.Node(9999) for i in nodes}
        self.distances[self.start].val = 0
        self.algorithm()
        self.tree = ""
        self.costs = ', '.join(["{}:{}".format(i,self.distances[i].val) for i in self.distances])


    @property
    def tree(self):
        return self._tree

    @tree.setter
    def tree(self,_):
        for i in self.distances:
            tree=current=i
            while(self.distances[current].prev != ''):
                current = self.distances[current].prev
                tree+=current            
            self.distances[i].tree = tree[::-1]
        self._tree = ', '.join([self.distances[i].tree for i in self.distances])

    def min(self):
        MIN=9999
        Letter = None 
        for i in self.distances:
            if( (i in self.unvisited) and (self.distances[i].val < MIN)):
                MIN = self.distances[i].val
                Letter = i
        return Letter,MIN

    def algorithm(self):
        while(self.unvisited != []):
            current, weight = self.min()
            for neighbor in self.links[current]:
                if neighbor in self.unvisited:
                    new_dist =self.links[current][neighbor]+weight
                    if(new_dist < self.distances[neighbor].val):
                        self.distances[neighbor].val = new_dist
                        self.distances[neighbor].prev = current
            self.unvisited.remove(current)
        
    def __str__(self) -> str:
        t = f"Shortest path tree for node {self.start}:\n{self.tree}\n"
        t+= f"Costs of the least-cost paths for node {self.start}:\n{self.costs}\n"
        return t

        



if __name__ == "__main__":
    nodes,links = get_file_data(fileinput.input())
    start_node = input("Please, provide the source node: ")
    Dj = Dijkstras(nodes,links,start_node)
    print(Dj)

    nodes,links = get_file_data(fileinput.input())
    Dv = Distace_Vector(nodes,links)
    Dv.bellman_ford()
    print(Dv)
  
    
    

    
    