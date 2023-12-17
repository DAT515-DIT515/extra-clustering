import networkx as nx
import csv
import matplotlib.pyplot as plt
import random
from sklearn.cluster import KMeans
import numpy as np
import sys


def mk_airportdict(FILE):
    airport_dict = {}
    with open(FILE, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        for line in csv_reader:
            airport_id = line[0]
            airport_info = line[1:]
            airport_dict[airport_id] = airport_info

    return airport_dict

def mk_routeset(FILE):
    with open(FILE, 'r', encoding='utf-8') as file:
        file = csv.reader(file)
        route_list = []

        for row in file:
            if "\\N" not in row:
                    departure = row[3]
                    destination = row[5]
                    route_list.append((departure, destination))
    return route_list

def mk_routegraph(airport_data, extracted_data):
    G = nx.DiGraph()

    # Add nodes to the graph using airport_data
    for airport_id, airport_info in airport_data.items():
        lat = airport_info[5]
        lon = airport_info[6]
        G.add_node(airport_id, lat=float(lat), lon=float(lon))

    # Add edges to the graph using extracted_data
    for edge in extracted_data:
        source_airport_id, destination_airport_id = edge
        if source_airport_id in airport_data.keys() and destination_airport_id in airport_data.keys():
            source_coords = (float(airport_data[source_airport_id][5]), float(airport_data[source_airport_id][6]))
            dest_coords = (float(airport_data[destination_airport_id][5]), float(airport_data[destination_airport_id][6]))
            distance = ((source_coords[0] - dest_coords[0]) ** 2 + (source_coords[1] - dest_coords[1]) ** 2) ** 0.5
            G.add_edge(source_airport_id, destination_airport_id, weight=distance)

    return G

def visualize_airports(graph):
    x = []
    y = []
    for airport_id, airport_info in airport_data.items():
            lat = airport_info[5]
            x.append(float(lat))
            lon = airport_info[6]
            y.append(float(lon))

    plt.scatter(y, x, s= 2)
    plt.show()

def visualize_plot_routes(routes):
    x = []
    y = []
    for airport_id, airport_info in airport_data.items():
            lat = airport_info[5]
            x.append(float(lat))
            lon = airport_info[6]
            y.append(float(lon))

    plt.scatter(y, x, s= 2)

    for edge in graph.edges():
        source_id, dest_id = edge
        source_coords = (float(airport_data[source_id][5]), float(airport_data[source_id][6]))
        dest_coords = (float(airport_data[dest_id][5]), float(airport_data[dest_id][6]))
        colors = ['red','yellow','green','purple']
        plt.plot([source_coords[1], dest_coords[1]], [source_coords[0], dest_coords[0]], color=random.choice(colors), alpha=0.5, linewidth=0.2)
    
    plt.show()

def k_spanning_tree(G, k=1000):

    # Convert the directed graph to an undirected graph
    undirected_graph = G.to_undirected()
    undirected_graph_copy = nx.create_empty_copy(undirected_graph)
    
    min_spanning_edges = list(nx.algorithms.tree.mst.minimum_spanning_edges(undirected_graph, algorithm='kruskal', data=True))
    sorted_edges = sorted(min_spanning_edges, key=lambda x: x[2].get('weight', 1), reverse=False)
    edges_to_keep = sorted_edges[:-k+1]
    undirected_graph_copy.add_edges_from(edges_to_keep)

    return undirected_graph_copy

def visualize_disconnected_clusters(graph):
    x = []
    y = []

    for node, data in graph.nodes(data=True):
        x.append(data['lat'])
        y.append(data['lon'])

    plt.scatter(y, x, s=1)

    for edge in graph.edges():
        source_coords = graph.nodes[edge[0]]
        dest_coords = graph.nodes[edge[1]]
        colors = ['red', 'yellow', 'green', 'purple']
        plt.plot(
            [source_coords['lon'], dest_coords['lon']],
            [source_coords['lat'], dest_coords['lat']],
            color=random.choice(colors),
            alpha=0.5,
            linewidth=1.5
        )

    plt.title('K-Spanning Tree Visualization')
    plt.show()

def k_means(data, k=7):
    
    data_array = np.array(data)
    kmeans = KMeans(n_clusters=k, random_state=0)
    labels = kmeans.fit_predict(data_array)

    return labels

def visualize_k_means(data, k=7):

    coordinates = [(float(info[5]), float(info[6])) for info in airport_data.values()]
    labels = k_means(coordinates, k)
    for i in range(k):
        cluster_points = np.array([coordinates[j] for j in range(len(coordinates)) if labels[j] == i])
        plt.scatter(cluster_points[:, 1], cluster_points[:, 0], s=0.2)

    plt.title(f'K-Means Clustering (k={k})')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.show()


if __name__ == '__main__':
    
    arg1 = sys.argv[1]
    AIRPORTS_FILE = 'airports.dat'
    ROUTES_FILE = 'routes.dat'
    
    airport_data = mk_airportdict(AIRPORTS_FILE)
    routes_list = mk_routeset(ROUTES_FILE)
    graph = mk_routegraph(airport_data, routes_list)

    if arg1 == 'airports':
        plt.figure(1)
        visualize_airports(airport_data)
    elif arg1 == 'routes':
        plt.figure(2)
        visualize_plot_routes(routes_list)
    elif arg1 == 'span':
        plt.figure(3)
        k_value = int(sys.argv[2])
        visualize_disconnected_clusters(k_spanning_tree(graph, k=k_value))
    elif arg1 == 'means':
        plt.figure(4)
        k_value = int(sys.argv[2])
        visualize_k_means(airport_data, k=k_value)
    else:
        print(f"Unknown argument: {arg1}")

    plt.show()


# Example usage:
# AIRPORTS_FILE = 'airports.dat'
# ROUTES_FILE = 'routes.dat'

# airport_data = mk_airportdict(AIRPORTS_FILE)
# routes = mk_routeset(ROUTES_FILE)
# graph = mk_routegraph(airport_data, routes)

# k = 1000
# k_spanning_tree_graph  = k_spanning_tree(graph, k)

# visualize_plot_routes(routes)
# visualize_disconnected_clusters(k_spanning_tree_graph)
# visualize_k_means(airport_data, k=7)

