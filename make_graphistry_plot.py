import os
import graphistry
import graph_builder as gb
graphistry.register(os.environ["GRAPHISTRY_KEY"])

def make_graphistry_plot(graph):
    graphistry.bind(source='src', destination='dst', node='nodeid').plot(graph)

graph = gb.build_directed_graph_from_csvs("data/", num_files=None)
make_graphistry_plot(graph)

