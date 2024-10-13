import typing

from graph_reader_yaml import GraphReader

OBJECT_WEIGHT = 10


class Robot:
    def __init__(self, graph_reader: GraphReader, graph, start_node: str, target_node: str):
        self.graph_reader = graph_reader
        self.current_node = start_node
        self.target_node = target_node
        self.graph = graph

    def move_to_next_node(self, next_node):
        pass

    # Could be in a PathCaluclator class
    def calculate_shortest_path(self):
        """returns next node to go to"""
        pass

    def move_object(self, next_node):
        print(f"Object between {self.current_node} and {next_node} is being moved.")

    # We need to make sure that our base graph has lettering that makes sense
    # e.g. from left to right for robot to turn & check in a way that makes sense
    def check_next_nodes(self):
        obstacles = self.graph_reader.read_obstacles()
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
