import networkx as nx
import numpy as np
from matplotlib import pyplot as plt
import glob
from cleaning_functions import clean_user_name
from networkx.algorithms import community as co

def build_directed_graph_from_csvs(path, sep=";,.", num_files=None):
    """
    API call for users to get a directed graph from the CSV files.

    path: the directory holding the csvs
    sep: the separator between users on each line
    num_files: how many files to use from dataset (none defaults to all)
    return graph: networkx graph object
    """
    return _build_graph_from_csvs(nx.DiGraph, path, sep, num_files)


def build_community_graph_from_csvs(path, sep=";,.", num_files=None):
    """
    API call for users to get an undirected graph from the CSV files.

    path: the directory holding the csvs
    sep: the separator between users on each line
    num_files: how many files to use from dataset (none defaults to all)
    return graph: networkx graph object
    """
    return _build_graph_from_csvs(nx.Graph, path, sep, num_files)

def _build_graph_from_csvs(type_of_graph, path, sep, num_files):
    """
    Backend function to process a series of CSVs in the format user1 -> user2
    separated by 'sep', and create a graph between the users.

    type_of_graph: Allows this function to work with either directed or undirected
    graphs, depending on provided method
    path: the directory holding the csvs
    sep: the separator between users on each line
    num_files: how many files to use from dataset (none defaults to all)
    return graph: networkx graph object
    """
    assert type(path)==str, "Path must be string type"

    if path[-1] == '/':
        path = path[:-1]

    file_list = glob.glob(path+'/*.csv')

    if not num_files:
        num_files = len(file_list)

    graph = type_of_graph()

    for file in file_list[:num_files]:
        print("Opening ", file)
        with open(file, 'r') as file_to_be_read:
            for line in file_to_be_read:
                user1, user2 = line.split(sep)
                user1 = clean_user_name(user1)
                user2 = clean_user_name(user2)
                if user1 != "NAN" and user2 != "NAN":
                    graph.add_edge(user1, user2)

    return graph

def draw_di_graph(graph_object, scale_by_degree=True, title=None):
    """
    Takes a networkx graph object and draws a plot of the network.

    graph_object: networkx graph object (directional or non)
    scale_by_degree: bool, changes drawn size of nodes to scale
    by number of connections (if True)

    return: postion map, network plot, axis object from matplotlib
    """
    plt.figure(dpi=150)
    positions = nx.spring_layout(graph_object)
    if scale_by_degree:
        d = nx.degree(graph_object)
        keys, degrees = zip(*d)
        network = nx.draw(graph_object, nodelist=keys,
                          node_size=[5*degree for degree in degrees],
                          pos=positions, alpha=0.5, arrows=False)
    else:
        network = nx.draw(graph_object, pos=positions, node_size=10, alpha=0.5)

    ax = plt.gca()
    if title:
        add_title_box_to_plot(ax, title)

    return positions, network, ax

def get_hub_nodes(graph_object, top_n_hubs=10):
    """
    Takes a graph and returns the nodenames for the
    n most connected nodes.

    graph_object: networkx graph object (directional or non)
    top_n_hubs: number of nodenames to return

    return: list of node names and their degrees as tuple (name, degree)
    """
    degrees = nx.degree(graph_object)
    sorted_degrees = sorted(degrees, key=lambda x: x[1], reverse=True)
    return sorted_degrees[:top_n_hubs]

def highlight_important_nodes(graph_object, positions, hub_nodes=None, top_n_hubs=10):
    """
    Given a graph object, this calculates the most important hubs,
    colors them in a different color, adds a label to each node,
    and makes a text box displaying the node name for each hub.

    graph_object: networkx graph object(directional or non)
    positions: Location map for nodes, based on one of the built in mappers for networkx
    top_n_hubs: Number of hubs to colorize and label

    return: None
    """

    # Figure out hub nodes if none are provided
    if not hub_nodes:
        hub_nodes = get_hub_nodes(graph_object, top_n_hubs=top_n_hubs)
    important_nodes, metric_value = zip(*hub_nodes)

    # Set up all the label dictionaries that networkx needs to properly id special nodes
    node_id = 1
    node_id_to_label = {}
    node_label_to_id = {}
    labels = {}
    for node in graph_object.nodes():
        if node in important_nodes:
            labels[node] = node
            node_id_to_label[node_id] = node
            node_label_to_id[node] = node_id
            node_id += 1

    # Drawing the special nodes to make them stand out
    nx.draw_networkx_nodes(graph_object, nodelist=important_nodes,
                           node_size=[10 * degree for degree in metric_value],
                           pos=positions, node_color='b', edgecolors='k')
    nx.draw_networkx_labels(important_nodes, positions, node_label_to_id, font_size=12,
                            font_color='w')

    # place a text box in upper left in axes coords
    textstr = '\n'.join(["{}: {}".format(idx+1, label) for idx, label in enumerate(important_nodes)])
    props = dict(boxstyle='round', facecolor='white', alpha=0.5)
    ax = plt.gca()
    ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=12,
            verticalalignment='top', bbox=props)

def get_communities(graph_object, iterations=5, print_communities=True):
    """
    Uses the community module (extension for networkx) to find communities
    in the graph. Uses Girvan Newman method:
    graph_object: Graph to detect communities in
    iterations: How many times to attempt community subdivision using Girvan Newman
    The more iterations, the more aggressive the algorithm is at breaking out communities
    into smaller chunks.

    return: Community map object, (dict)
    """
    communities_map = {}

    community_generator = co.girvan_newman(graph_object)
    for _ in range(iterations):
        communities = next(community_generator)

    for ix, community_list in enumerate(communities):
        if print_communities:
            print(community_list)
        if len(community_list) > 5:
            node_id = ix + 1
        else:
            node_id = 0
        for node in community_list:
            communities_map[node] = node_id

    return communities_map

def draw_community_map(graph_object, communities, title=None):
    """
    Given a graph object, the positions of the nodes, and the community label
    for each node, colorize the communities

    graph_object: Graph to draw
    communities: Community Map (dict of form {node: community_id})

    return: node positions, network object, axis
    """

    num_communities = max(communities.values())
    colors = []

    for node_name in graph_object.nodes():
        if communities[node_name]:
            colors.append(communities[node_name]+10)
        else:
            colors.append(0)

    plt.figure(dpi=150)
    positions = nx.spring_layout(graph_object)
    network = nx.draw(graph_object, node_size=5, pos=positions,
                      node_color=plt.cm.jet(colors), alpha=0.9)

    ax = plt.gca()
    if title:
        add_title_box_to_plot(ax, title)

    return positions, network, ax

def add_title_box_to_plot(ax, title):
    """
    Adds a string to the bottom of the plots inside a bounding box.

    ax: the axis containing the graph plot
    title: string to add inside the bounding box on the plot

    return: None
    """
    props = dict(boxstyle='round', facecolor='white', alpha=0.5)
    ax.text(0.25, 0.05, title, transform=ax.transAxes, fontsize=12,
            verticalalignment='top', bbox=props)