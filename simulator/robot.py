from graph_reader_yaml import GraphReader
from path_calculator import PathCalculator

OBJECT_WEIGHT = 10


class Robot:
    def __init__(self, graph_reader: GraphReader, graph, start_node: str, target_node: str, path_calculator: PathCalculator):
        self.graph_reader = graph_reader
        self.current_node = start_node
        self.target_node = target_node
        self.path_calculator = path_calculator
        self.graph = graph

    def has_reached_target(self):
        return self.current_node == self.target_node

    def move_to_next_node(self):
        next_node = self.get_next_node()
        print(f"Moving from {self.current_node} to {next_node}")
        self.current_node = next_node

    def get_next_node(self):
        next_node = self.path_calculator.get_next_node(graph=self.graph, start=self.current_node, target=self.target_node)
        print(f"The next node considering the shortest path is node {next_node}")
        return next_node

    def move_object(self, next_node):
        print(f"Object between {self.current_node} and {next_node} is being moved.")

    # We need to make sure that our base graph has lettering that makes sense
    # e.g. from left to right for robot to turn & check in a way that makes sense
    def check_next_nodes(self):
        obstacles = self.graph_reader.read_obstacles()
        neighbors = self.get_neighbors()
        print(f"[ET] I am now infront of my next node {self.current_node}. I will now check for the next {len(neighbors)} connections.")

        for neighbor in neighbors:
            check_connections = {neighbor, self.current_node}
            if any(check_connections.issubset(set(sublist)) for sublist in obstacles["barrier"]):
                print(f"There is a movable object between node {self.current_node} and {neighbor}.")
                self.increase_weight_for_edge_with_obstacle(neighbor)
            if any(check_connections.issubset(set(sublist)) for sublist in obstacles["missing_line"]):
                print(f"There is a missing line between connection {self.current_node} and {neighbor}.")
                self.remove_edge(neighbor)
            if neighbor in obstacles["cone"]:
                print(f"Pylon on {neighbor}.")
                self.remove_node(neighbor)

    def increase_weight_for_edge_with_obstacle(self, node):
        self.graph[self.current_node] = [{k: v + OBJECT_WEIGHT if k == node else v for k, v in neighbor.items()} for neighbor in self.graph[self.current_node]]
        self.graph[node] = [{k: v + OBJECT_WEIGHT if k == self.current_node else v for k, v in neighbor.items()} for neighbor in self.graph[node]]
        print(f"Weight between {self.current_node} and {node} has been raised by {OBJECT_WEIGHT}.")
    
    def remove_node(self, node_to_remove):
        del self.graph[node_to_remove]
        for node, edges in self.graph.items():
            edges = [d for d in edges if node_to_remove not in d]
            self.graph[node] = edges
        print(f"Removed node {node_to_remove} including all its edges.")

    def remove_edge(self, neighbor):
        self.graph[self.current_node] = [item for item in self.graph[self.current_node] if not (isinstance(item, dict) and neighbor in item)]
        self.graph[neighbor] = [item for item in self.graph[neighbor] if not (isinstance(item, dict) and self.current_node in item)]
        print(f"Removed edge between {neighbor} and {self.current_node}.")

    def get_neighbors(self):
        neighboring_nodes = self.graph[self.current_node]
        return [list(n.keys())[0] for n in neighboring_nodes]
