import networkx as nx
import csv
import haversine as hs
import matplotlib.pyplot as plt
import random

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
        G.add_node(airport_id, lat = float(lat), lon = float(lon))

    # Add edges to the graph using extracted_data
    for edge in extracted_data:
        source_airport_id, destination_airport_id = edge
        if source_airport_id in airport_data.keys() and destination_airport_id in airport_data.keys():
            G.add_edge(source_airport_id, destination_airport_id)
 
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


# Example usage:
airport_data = mk_airportdict(AIRPORTS_FILE)
routes = mk_routeset(ROUTES_FILE)
graph = mk_routegraph(airport_data, routes)