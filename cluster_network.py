import networkx as nx
import csv
import haversine as hs
import matplotlib.pyplot as plt


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
    G = nx.Graph()

    # Add nodes to the graph using airport_data
    for airport_id, airport_info in airport_data.items():
        
        lat = airport_info[5]

        lot = airport_info[6]

        G.add_node(airport_id, lat = float(lat), lot = float(lot))

    # Add edges to the graph using extracted_data
    for edge in extracted_data:
        source_airport_id, destination_airport_id = edge
        G.add_edge(source_airport_id, destination_airport_id)

    return G

# Example usage:
AIRPORTS_FILE = 'airports.dat'
ROUTES_FILE = 'routes.dat'

airport_data = mk_airportdict(AIRPORTS_FILE)

routes = mk_routeset(ROUTES_FILE)

graph = mk_routegraph(airport_data, routes)

#print(graph.edges())
print(graph.nodes.data())

# Visualize the graph (optional)
#  # You can change the layout as needed
# nx.draw(graph)
# plt.show()
