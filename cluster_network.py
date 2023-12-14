import networkx as nx
import csv
import matplotlib.pyplot as plt
import random
from math import cos, sqrt, pi


AIRPORTS_FILE = 'airports.dat'
ROUTES_FILE = 'routes.dat'

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

            # Calculate distance as the weight attribute
            distance = ((source_coords[0] - dest_coords[0]) ** 2 + (source_coords[1] - dest_coords[1]) ** 2) ** 0.5
            G.add_edge(source_airport_id, destination_airport_id, weight=distance)

    return G

def plot_routes(routegraph):
    x = []
    y = []
    for airport_id, airport_info in airport_data.items():
            lat = airport_info[5]
            x.append(float(lat))
            lon = airport_info[6]
            y.append(float(lon))

    plt.scatter(y, x, s= 2)

    # Draw edges on the scatter plot
    for edge in graph.edges():
        source_id, dest_id = edge
        source_coords = (float(airport_data[source_id][5]), float(airport_data[source_id][6]))
        dest_coords = (float(airport_data[dest_id][5]), float(airport_data[dest_id][6]))
        colors = ['red','yellow','green','purple']
        plt.plot([source_coords[1], dest_coords[1]], [source_coords[0], dest_coords[0]], color=random.choice(colors), alpha=0.5, linewidth=0.2)

    # To show the plot
    plt.show()

def k_spanning_tree(G, k=1000):

    # Convert the directed graph to an undirected graph
    undirected_graph = G.to_undirected()
    min_spanning_edges = list(nx.minimum_spanning_edges(undirected_graph, algorithm='kruskal', data=False))
    sorted_edges = sorted(G.edges(data=True), key=lambda x: x[2].get('weight', 1), reverse=True)
    edges_to_remove = sorted_edges[:k-1]
    new_graph = G.copy()
    new_graph.remove_edges_from(edges_to_remove)

    return new_graph

def visualize_graph(graph):
    x = []
    y = []

    for node, data in graph.nodes(data=True):
        x.append(data['lat'])
        y.append(data['lon'])

    plt.scatter(y, x, s=2)

    for edge in graph.edges():
        source_coords = graph.nodes[edge[0]]
        dest_coords = graph.nodes[edge[1]]
        colors = ['red', 'yellow', 'green', 'purple']
        plt.plot(
            [source_coords['lon'], dest_coords['lon']],
            [source_coords['lat'], dest_coords['lat']],
            color=random.choice(colors),
            alpha=0.5,
            linewidth=0.2
        )

    plt.title('K-Spanning Tree Visualization')
    plt.show()


# Example usage:
airport_data = mk_airportdict(AIRPORTS_FILE)
routes = mk_routeset(ROUTES_FILE)
graph = mk_routegraph(airport_data, routes)
# print(graph)

# Call the k_spanning_tree function
k = 1000  # You can adjust k as needed
k_spanning_tree_graph  = k_spanning_tree(graph, k)
# print(k_spanning_tree_graph)

# Visualize the resulting graph
visualize_graph(k_spanning_tree_graph )
# plot_graph(k_spanning_tree_graph, airport_data)











# def plot_graph(graph, airport_data):
#     x = []
#     y = []
#     for airport_id, airport_info in airport_data.items():
#         lat = airport_info[5]
#         x.append(float(lat))
#         lon = airport_info[6]
#         y.append(float(lon))

#     plt.scatter(y, x, s=2)

#     # Draw edges on the scatter plot
#     for edge in graph.edges(data=True):
#         source_id, dest_id, edge_data = edge
#         source_coords = (float(airport_data[source_id][5]), float(airport_data[source_id][6]))
#         dest_coords = (float(airport_data[dest_id][5]), float(airport_data[dest_id][6]))

#         # Access the 'weight' attribute for color
#         weight = edge_data.get('weight', 1)

#         colors = ['red', 'yellow', 'green', 'purple']
#         plt.plot([source_coords[1], dest_coords[1]], [source_coords[0], dest_coords[0]],
#                  color=random.choice(colors), alpha=0.5, linewidth=0.2)

#     # To show the plot
#     plt.title('k-Spanning Tree Visualization')
#     plt.show()



# def distance_between_edges(edges, ap1, ap2):

#     r = 6371.0   # Radius of Earth km
#     lat_1 = edges[ap1]['lat'] * pi/180
#     lon_1 = edges[ap1]['lon'] * pi/180
#     lat_2 = edges[ap2]['lat'] * pi/180
#     lon_2 = edges[ap2]['lon'] * pi/180
#     dlat = lat_2 - lat_1
#     dlon = lon_2 - lon_1
#     meanlat = (lat_1 + lat_2) / 2
    
#     distance = r* sqrt(dlat **2 + (cos(meanlat) * dlon) **2 )
    
#     return distance

# def set_edge_weights(graph, distance_function):
#     for edge in graph.edges():
#         source_id, dest_id = edge
#         distance = distance_function(graph.nodes, source_id, dest_id)
#         graph[source_id][dest_id]['weight'] = distance