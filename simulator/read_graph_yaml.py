import yaml

OBJECT_WEIGHT = 10

class GraphReaderYAML:
    # TODO: Robot class that has current node/target node instaed of the reader?
    graph = {}
    current_node = "H"


    def read_base_graph(self):
        """
        Robot knows this from the start.
        """
        with open('graph_configs/base_graph.yml', 'r') as file:
            self.graph = yaml.safe_load(file)

    def read_graph_with_obstacles(self):
        """
        Simulates the robot looking at the graph in reallife
        """
        with open('graph_configs/obstacles.yml', 'r') as file:
            obstacles = yaml.safe_load(file)
        return obstacles

    # TODO: also into a Robot class with drive, moveobj, ...
    # We need to make sure that our base graph has lettering that makes sense
    # e.g. from left to right for robot to turn & check in a way that makes sense
    def check_next_nodes(self):
        obstacles = self.read_graph_with_obstacles()
        neighbors = obstacles[self.current_node]

        for neighbor in neighbors:
            for node, edge in neighbor.items():
                if isinstance(edge, list) and 'O' in edge:
                    print(f"There is a movable object between node {self.current_node} and {node}.")
                    self.increase_weight_for_edge_with_obstacle(node)
                if "P" in obstacles[node]:
                    print(f"Pylon on {node}.")
                    self.remove_node(node)

    def increase_weight_for_edge_with_obstacle(self, node):
        # TODO: I am sure this could be done better
        self.graph[self.current_node] = [{k: v + OBJECT_WEIGHT if k == node else v for k, v in neighbor.items()} for neighbor in self.graph[self.current_node]]
        self.graph[node] = [{k: v + OBJECT_WEIGHT if k == self.current_node else v for k, v in neighbor.items()} for neighbor in self.graph[node]]
        print(f"Weight between {self.current_node} and {node} has been raised by {OBJECT_WEIGHT}.")
    
    def remove_node(self, node_to_remove):
        del self.graph[node_to_remove]
        for node, edges in self.graph.items():
            edges = [d for d in edges if node_to_remove not in d]
            self.graph[node] = edges
        print(f"Removed node {node_to_remove} including all its edges.")
