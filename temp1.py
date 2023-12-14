import networkx as nx
import csv
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


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

        # G.add_node(airport_id, lat = float(lat), lot = float(lot))
        G.add_node(airport_id, pos=(lon, lat))

    # Add edges to the graph using extracted_data
    for edge in extracted_data:
        source_airport_id, destination_airport_id = edge
        if source_airport_id in airport_data.keys() and destination_airport_id in airport_data.keys():
            G.add_edge(source_airport_id, destination_airport_id)
    return G

# Example usage:
AIRPORTS_FILE = 'airports.dat'
ROUTES_FILE = 'routes.dat'

airport_data = mk_airportdict(AIRPORTS_FILE)

routes = mk_routeset(ROUTES_FILE)

graph = mk_routegraph(airport_data, routes)

# print(len(graph.edges()))
#print(len(graph.nodes.data()))

# def plot_airports(airport_data):
#     x = []
#     y = []
#     for airport_id, airport_info in airport_data.items():
#         lat = airport_info[5]
#         x.append(float(lat))
#         lot = airport_info[6]
#         y.append(float(lot))

#     data = {'Latitude': x, 'Longitude': y}
#     df = pd.DataFrame(data)
#     plt.figure(figsize=(12, 6))
#     sns.scatterplot(x='Longitude', y='Latitude', data=df, s=8)
#     plt.title('Airports Scatter Plot')
#     plt.show()

# def plot_routes(routegraph):
#     x = []
#     y = []
#     for airport_id, airport_info in airport_data.items():
#         lat = airport_info[5]
#         x.append(float(lat))
#         lot = airport_info[6]
#         y.append(float(lot))

#     data = {'Latitude': x, 'Longitude': y}
#     df = pd.DataFrame(data)
#     plt.figure(figsize=(12, 6))
#     sns.scatterplot(x='Longitude', y='Latitude', data=df, s=4)
#     plt.title('Airports Scatter Plot')

#     G = mk_routegraph(airport_data, routes)
#     pos = {node: (float(airport_data[node][6]), float(airport_data[node][5])) for node in G.nodes}
#     plt.figure(figsize=(12, 6))
#     nx.draw(G, pos, with_labels=False, node_size=8, edge_color='gray', alpha=0.5)
#     plt.title('Routes')
#     plt.show()

def plot_routes(routegraph):
    # Scatter plot of airport data points
    x = []
    y = []
    for airport_id, airport_info in airport_data.items():
        lat = airport_info[5]
        x.append(float(lat))
        lon = airport_info[6]
        y.append(float(lon))  # Corrected variable name from 'lot' to 'lon'

    data = {'Latitude': x, 'Longitude': y}
    df = pd.DataFrame(data)
    sns.scatterplot(x='Longitude', y='Latitude', data=df, s=4, zorder=2)  # Use zorder to control the order of plotting

    # Plot the networkx graph with edges
    G = mk_routegraph(airport_data, routes)
    pos = {node: (float(airport_data[node][6]), float(airport_data[node][5])) for node in G.nodes}
    plt.figure(figsize=(12, 6))
    nx.draw(G, pos, with_labels=False, node_size=8, edge_color='gray', alpha=0.5, zorder=1)  # Use zorder to control the order of plotting
    plt.title('Routes')

    plt.show()

plot_routes(graph)
