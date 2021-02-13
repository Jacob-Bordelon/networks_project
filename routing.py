import fileinput


def get_min(verticies, unvisited):
    MIN = 9999 # set default MIN to infinity
    Letter = None
    for i in verticies:
        if i in unvisited:
            if(verticies[i]["val"] < MIN):
                MIN = verticies[i]["val"]
                Letter = i     
    return Letter,MIN

def dijkstras_algorithm(links,start_node:str)->dict:
    unvisited = links["ends"]

    # let distance of all other vertices from start = infinity
    distances = {i:{"val":9999,"prev":"","tree":""} for i in unvisited}
    distances[start_node]["val"] = 0

    while(unvisited != []):
        current_vertex,weight = get_min(distances,unvisited)
        for neighbor in links[current_vertex]:
            if neighbor in unvisited:
                new_dist = links[current_vertex][neighbor]["val"] + weight
                if new_dist < distances[neighbor]["val"]:
                    distances[neighbor]["val"] = new_dist
                    distances[neighbor]["prev"] = current_vertex
        unvisited.remove(current_vertex)

    return distances

def get_trees(distances:dict)->None:
    for i in distances:
        tree=current=i
        while(distances[current]["prev"] != ''):
            current = distances[current]["prev"]
            tree+=current            
        distances[i]["tree"] = tree[::-1]
    


if __name__ == "__main__":
    
    # Get user input
    start_node = input("Please, provide the source node: ")

    # Get file input
    links = {}
    for line in fileinput.input():
        node = line.rstrip("\n").split(",")
        if(node[0]==''):
            links.update({"ends":node[1:]})
        else:
            links.update({node[0]:{links["ends"][i]:{"val":int(node[i+1]),"prev":""} for i in range(len(links["ends"]))}})

    #  Dijkstra’s algorithm
    shortest_paths = dijkstras_algorithm(links,start_node)
    get_trees(shortest_paths) # Get the path-trees

    trees = ', '.join([shortest_paths[i]["tree"] for i in shortest_paths])
    print(f"Shortest path tree for node {start_node}:\n{trees}")

    costs = ', '.join(["{}:{}".format(i,shortest_paths[i]["val"]) for i in shortest_paths])
    print(f"Costs of the least-cost paths for node {start_node}:\n{costs}")
    print()
    
    # Bellman-Ford equation

    