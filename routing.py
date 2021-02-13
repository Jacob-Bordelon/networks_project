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
    
def BellmanFord(V, graph, src, nodes): 
	dist = {}
	for n in nodes:
		dist[n] = float("Inf")
	
	dist[src] = 0
	
	
	for _ in range(V - 1): 
		for u, v, w in graph: 
			if dist[u] != float("Inf") and dist[u] + w < dist[v]: 
				dist[v] = dist[u] + w 
	
	for u, v, w in graph: 
		if dist[u] != float("Inf") and dist[u] + w < dist[v]: 
			print("Graph contains negative weight cycle") 
			return
					
	dists = ' '.join(str(dist[n]) for n in nodes)
	print("Distance vector for node " + src + ": " + dists)

if __name__ == "__main__":
    
    # Get user input
	start_node = input("Please, provide the source node: ")

    # Get file input
	links = {}
	for line in fileinput.input():
		node = line.rstrip("\n").split(",")
		if(node[0]==''):
			links.update({"ends":node[1:]})
			nodes = node[1:]
		else:
			links.update({node[0]:{links["ends"][i]:{"val":int(node[i+1]),"prev":""} for i in range(len(links["ends"]))}})
	#  Dijkstra’s algorithm
	tmp = links
	graph = []
	
	
	for node in list(tmp.keys())[1:]:
		for elem in tmp[node].keys():
			if tmp[node][elem]['val'] != 0:
				graph.append([node, elem, tmp[node][elem]['val']])
	shortest_paths = dijkstras_algorithm(links,start_node)
	get_trees(shortest_paths) # Get the path-trees
	trees = ', '.join([shortest_paths[i]["tree"] for i in shortest_paths])
	print(f"Shortest path tree for node {start_node}:\n{trees}")
	costs = ', '.join(["{}:{}".format(i,shortest_paths[i]["val"]) for i in shortest_paths])
	print(f"Costs of the least-cost paths for node {start_node}:\n{costs}")

	# Bellman-Ford equation
	for n in nodes:
                BellmanFord(len(nodes), graph, n, nodes)
	
	
