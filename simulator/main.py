from read_graph_yaml import GraphReaderYAML


if __name__ == '__main__':
    graph_reader = GraphReaderYAML()
    graph_reader.read_base_graph()
    graph_reader.check_next_nodes()