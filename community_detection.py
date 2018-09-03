import graph_builder as gb
import matplotlib.pyplot as plt


def find_communities_in_csv_network_files(num_files = None, file_name=None, plot_title=None, iterations=5,
                                          print_communities=False):
    """
    Controller function for the analysis process. User provides a few settings
    and this function will load the graph, setup all edges and nodes, find communities,
    and make a plot.

    num_files: how many of the CSV files to read, None defaults to read all
    file_name: string, if provided, saves the network graph to file, otherwise shows the plot
    plot_title: label for plot, if needed (string)
    print_communities: bool, whether to print members of each community to terminal

    return: None
    """
    graph = gb.build_community_graph_from_csvs("data/", num_files=num_files)
    communities = gb.get_communities(graph, iterations=iterations, print_communities=print_communities)
    gb.draw_community_map(graph, communities, title=plot_title)

    if type(file_name) == str:
        plt.savefig(file_name, dpi=150)
    else:
        plt.show()

if __name__ == "__main__":
    find_communities_in_csv_network_files(file_name="images/community_detection_example.png", num_files=3,
                                          plot_title="Communities in Twitter 'Trump' Discussions",
                                          iterations=30, print_communities=True)
