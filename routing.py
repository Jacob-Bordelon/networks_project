import fileinput

NODES = []
LINKS = {}
# --------------- Stuff for DIJKSTRA’S ALGORITHM ------------------
# Recursevly find the tree
def recur(p,source,i):
    if i == source:
        return source
    return recur(p,source,p[i])+i

# get the trees from the previos
def format_tree(p,source):
    T = {}
    for i in p:
        T[i]=recur(p,source,i)
    return T


def dijstraks_algorithm(nodes:list, links:dict, source:str):
    # Initialzation
    index = lambda u: nodes.index(u)
    getmin = lambda D : min([i for i in D.items() if i[0] not in N],key=lambda x: x[1])[0]

    N=[source]
    D={}
    p={}
    for i in links:
        if links[source][index(i)] != 9999:
            D[i] = cost(source,i)
            p[i] = source
        else:
            D[i] = 9999
    p[source]=""
    
    # Repeat until all nodes are in N
    while len(N) != len(nodes):
        # find w not in N such that D(w) is a minimum
        w = getmin(D)

        # add w to N
        N.append(w)

        # update D(v) for all v adjacent to w and not in N
        for v in links:
            if v not in N:
                if (D[w]+cost(w,v)) < D[v]:
                    D[v] = (D[w]+cost(w,v))
                    p[v] = w
    
    # format shortest path trees
    P = format_tree(p,source)

    return D,P

# --------------- Stuff for DISTANCE-VECTOR ALGORITHM ------------------




class Node(object):
    # set neighbors so the nodes can communicate
    destinations = {}

    # initialize the node
    def __init__(self,name) -> None:
        self.name = name
        self.Dx = self.Cx = {i:cost(name,i) for i in NODES}
        self.Dv = {i:{a:9999 for a in NODES} for i in NODES}
        self.Dv[self.name] = self.Dx
        self.neighbors = [i for i in self.Dx if i != name and self.Cx[i] != 9999]

        Node.destinations.update({name:self})
        self.sendout()

    # When the Dv changes, perform the bellman ford algorithm
    def setDv(self,w,val):
        self.Dv[w] = val
        self.bellman(w)

    # send distance vector to each neighbor(w)
    def sendout(self):     
        for w in self.neighbors:
            if w in Node.destinations:
                V = Node.destinations[w]
                # Get the neighbors distance vector
                self.setDv(V.name,V.Dx)
                # Send out your own distance vector
                V.setDv(self.name,self.Dx)
    
    # Bellman ford algorithm
    def bellman(self,v):
        for y in self.Dx:
            if (self.Cx[v] + self.Dv[v][y]) < self.Dx[y]:
                self.Dx[y] = (self.Cx[v] + self.Dv[v][y])
                self.sendout()

    # Display as an output
    def __str__(self) -> str:
        return ', '.join([str(self.Dx[i]) for i in self.Dx])


def distance_vector():
    return {i:Node(i) for i in NODES}
    
# --------------- Main  ------------------

if __name__ == "__main__":
    # get source 
    source = input("Please, provide the source node: ")
    # get information from .csv file
    data = fileinput.input()
    # format data to a graph format
    nodes = data.readline().rstrip("\n").split(",")[1:]
    links = [i.rstrip("\n").split(",") for i in data]
    links = {i[0]:[int(a) for a in i[1:]] for i in links}

    NODES = nodes 
    LINKS = links

    cost = lambda u,v: links[u][nodes.index(v)]
    
    # dijstraks algorithm - Jacob
    
    result = dijstraks_algorithm(nodes,links,source)
    costs = ', '.join([f"{i}:"+str(result[0][i]) for i in result[0]])
    result[1].pop(source)
    tree = sorted([result[1][i] for i in result[1]],key=len)
    tree = ', '.join(tree)
    print(f"Shortest path tree for node {source}:\n{tree}")
    print(f"Costs of the least-cost paths for node {source}:\n{costs}\n")
 

    # distance vector algorithm - JonMichael
    result = distance_vector()
    for i in result:
        print(f"Distance vector for node {i}: {result[i]}")



