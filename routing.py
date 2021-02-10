import fileinput
from typing import NewType


# get valuses from csv file
links = {}


def get_shortest_distance(current,visited=[],score=0):
    vertecies = {}
    for i in range(len(links["ends"])):
        if(links["ends"][i] not in visited):
            if (int(links[current][i]) != 9999):
                vertecies.update({ links["ends"][i] : int(links[current][i])+score })
            else:
                vertecies.update({ links["ends"][i] : int(links[current][i]) })
    
    return vertecies

def compare_distance(old,new):
    for i in new:
        if(i in old and new[i] < old[i]):
            old[i] = new[i]

def get_min(verticies, visited):
    MIN = 9999
    Letter = None
    for i in verticies:
        if i not in visited:
            if (verticies[i] < MIN):
                MIN = verticies[i]
                Letter = i
    return Letter,MIN

def shortest_path(a):
    # initialize visited nodes, current vertex, and current score
    unvisited = links["ends"]

    shortest_distance = get_shortest_distance(a)
    visited = [a]
    unvisited.remove(a)
    current,score = get_min(shortest_distance,visited)

    while(unvisited != []):
        unvisited.remove(current)
        visited.append(current)
        new_distance = get_shortest_distance(current,visited,score)
        compare_distance(shortest_distance, new_distance)
        current,score = get_min(shortest_distance,visited)

    return shortest_distance
        
        

if __name__ == "__main__":
    
    # Get user input
    start_node = input("Please, provide the source node: ")

    # Get file input
    for line in fileinput.input():
        node = line.rstrip("\n").split(",")
        if(node[0]==''):
            links.update({"ends":node[1:]})
        else:
            links.update({node[0]:node[1:]})

    #  Dijkstra’s algorithm
    print(shortest_path(start_node))

    # Bellman-Ford equation

    