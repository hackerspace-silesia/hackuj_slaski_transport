import osmnx as ox
G = ox.graph_from_place('Dabrowa Gornicza')
ox.plot_graph(ox.project_graph(G), node_size=0, edge_color='k')