from fileinput import filename
import networkx as nx
import sys
import operator
import time

def Vertex_order(Graph):
    dic = nx.pagerank(Graph)
    return list(map(lambda x: x[0],sorted(dic.items(), key = operator.itemgetter(1), reverse=True)))

def link_aggregate(Graph):
	clusters = []
	vertices = Vertex_order(Graph)
 #For each vertex check if it belongs to the existing clusters
	for vertex in vertices:
		added = False
		for x in range(len(clusters)):
			new_cluster = clusters[x] + [vertex]
			new_cluster_weight = float(2 * nx.number_of_edges(Graph.subgraph(new_cluster)) / nx.number_of_nodes(Graph.subgraph(new_cluster)))
			weight1 = float(2 * nx.number_of_edges(Graph.subgraph(clusters[x])) / nx.number_of_nodes(Graph.subgraph(clusters[x])))
			#If vertex belongs to the cluster, add it
			if new_cluster_weight > weight1:
				clusters[x] += [vertex]
				added = True
		#If vertex does not belong to any cluster then create new cluster
		if added == False:
			clusters.append([vertex])
	return clusters

def iterative_search(cluster,Graph):
	#Create a subgraph
	current_graph = Graph.subgraph(cluster)
 #Calculate density
	weig = float(2*nx.number_of_edges(current_graph)/nx.number_of_nodes(current_graph))
	increased = True
	while increased:
		node_list = list(current_graph.nodes)
	#For each vertex, find all adjacent vertices
		for vertex in current_graph.nodes:
			adjacency = Graph.neighbors(vertex)
			node_list = list(set(node_list).union(set(adjacency)))
	 #For each vertex, calculate community density and check for change in density
		for vertex in node_list:
			old_vert = list(current_graph.nodes)
			if vertex in old_vert:
				old_vert.remove(vertex)
			else:
				old_vert.append(vertex)
			if not old_vert:
				new_current_weig=0
			else:
				new_cur = Graph.subgraph(old_vert)
				new_current_weig = float(2 * nx.number_of_edges(new_cur) / nx.number_of_nodes(new_cur))
			cur_weig = float(2 * nx.number_of_edges(current_graph) / nx.number_of_nodes(current_graph))
			if new_current_weig > cur_weig:
				current_graph = new_cur.copy()
		new_weight = float(2 * nx.number_of_edges(current_graph) / nx.number_of_nodes(current_graph))
		#If new density does not change, then stop
		if new_weight == weig:
			increased = False
		else:
			weig = new_weight
	return list(current_graph.nodes)

def community(file_name,Total_clusters):
    #Read input file
    graph_file = open(file_name)
    edges = graph_file.read().splitlines()
    #Generate graph
    graph = nx.Graph()
    for edge in edges:
        v = edge.split()
        graph.add_edge(int(v[0]),int(v[1]))
    #Generate clusters using link aggregate algo
    clusters = link_aggregate(graph)
    #Generate a cluster that is local maxima by using Improved Iterative Scan Algorithm
    for cluster in clusters:
        iterative_graph = sorted (iterative_search(cluster, graph))
        if iterative_graph not in Total_clusters:
            Total_clusters.append(iterative_graph)
    return Total_clusters

def main():
    file_name = sys.argv[1]
    Total_clusters = []
    result =community(file_name,Total_clusters)
    print(len(result))
    print(result)
    #Write output to filename_out file
    with open(file_name.split(".")[0]+"_out.txt", 'a') as file:
        i=0
        for clus in Total_clusters:
          i=i+1
          communities = " ".join(map(str, clus))
          file.write(communities+ '\n')
    
if __name__ == "__main__":
    start_time=time.time()
    main()
    end_time=time.time()
    print("Total time="+str(end_time-start_time))


