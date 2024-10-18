import yaml


class GraphReader:
    def read_base_graph(self):
        """
        Reads and returns the base graph that we already know.
        """
        pass

    def read_obstacles(self):
        """
        Reads the obstacles on the graph. In the simulation reads all of them
        while in the real robot, it would only read the ones on the next edges.
        """
        pass


class GraphReaderYAML(GraphReader):
    def read_base_graph(self):
        with open('graph_configs/base_graph.yml', 'r') as file:
            return yaml.safe_load(file)

    def read_obstacles(self):
        """
        Simulates the robot looking at the graph in reallife.
        """
        with open('graph_configs/obstacles.yml', 'r') as file:
            obstacles = yaml.safe_load(file)
        return obstacles

