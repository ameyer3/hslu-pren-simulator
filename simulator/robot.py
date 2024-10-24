from simulator.graph_reader_yaml import GraphReader
from simulator.path_calculator import PathCalculator

OBJECT_WEIGHT = 10


class Robot:
    reweighted_edges = []
    previous_path = []

    def __init__(
        self, graph_reader: GraphReader, graph, start_node: str, target_node: str, path_calculator: PathCalculator
    ):
        self.graph_reader = graph_reader
        self.current_node = start_node
        self.target_node = target_node
        self.path_calculator = path_calculator
        self.graph = graph

    def has_reached_target(self):
        return self.current_node == self.target_node

    def move_to_next_node(self, neighbors):
        next_node, node_position = self.get_next_node_position(neighbors)
        print(f"Moving from {self.current_node} to {next_node} which is the {node_position} edge from left to right.")
        self.previous_path.append(self.current_node)
        self.current_node = next_node

    def get_next_node(self):
        next_node = self.path_calculator.get_next_node(
            graph=self.graph, start=self.current_node, target=self.target_node
        )
        print(f"The next node considering the shortest path is node {next_node}")
        return next_node
    

    def get_next_node_position(self, neighbors):
        next_node = self.get_next_node()
        target_index = neighbors.index(next_node)
        if len(self.previous_path) != 0:
            start_index = neighbors.index(self.previous_path[-1])
            edges_to_target = (target_index - start_index) % len(neighbors)
        else:
            edges_to_target = target_index + 1

        return next_node, edges_to_target

    def move_object(self, next_node):
        print(f"Object between {self.current_node} and {next_node} is being moved.")

    def check_next_nodes(self):
        obstacles = self.graph_reader.read_obstacles()
        neighbors = (self.get_neighbors())
        unvisited_neighbors = self.get_unvisited_nodes(neighbors)
        print(
            f"[ET] I am now infront of my next node {self.current_node}. I will now check for the next {len(unvisited_neighbors)} connections."
        )

        for neighbor in unvisited_neighbors:
            check_connections = {neighbor, self.current_node}
            if any(check_connections.issubset(set(sublist)) for sublist in obstacles["barrier"]):
                print(f"There is a movable object between node {self.current_node} and {neighbor}.")
                self.increase_weight_for_edge_with_obstacle(neighbor)
            if any(check_connections.issubset(set(sublist)) for sublist in obstacles["missing_line"]):
                print(f"There is a missing line between connection {self.current_node} and {neighbor}.")
                self.remove_edge(neighbor)
                neighbors.remove(neighbor)
            if neighbor in obstacles["cone"]:
                print(f"Pylon on {neighbor}.")
                self.remove_node(neighbor)
        return neighbors

    def increase_weight_for_edge_with_obstacle(self, node):
        if [node, self.current_node] not in self.reweighted_edges:
            self.graph[self.current_node] = [
                {k: v + OBJECT_WEIGHT if k == node else v for k, v in neighbor.items()}
                for neighbor in self.graph[self.current_node]
            ]
            self.graph[node] = [
                {k: v + OBJECT_WEIGHT if k == self.current_node else v for k, v in neighbor.items()}
                for neighbor in self.graph[node]
            ]
            print(f"Weight between {self.current_node} and {node} has been raised by {OBJECT_WEIGHT}.")
            self.reweighted_edges += [self.current_node, node], [node, self.current_node]
            print(self.reweighted_edges)
        else:
            print("Barrier has already been detected and taken into account.")

    def remove_node(self, node_to_remove):
        del self.graph[node_to_remove]
        for (
            node,
            edges,
        ) in self.graph.items():
            edges = [d for d in edges if node_to_remove not in d]
            self.graph[node] = edges
        print(f"Removed node {node_to_remove} including all its edges.")

    def remove_edge(self, neighbor):
        self.graph[self.current_node] = [
            item for item in self.graph[self.current_node] if not (isinstance(item, dict) and neighbor in item)
        ]
        self.graph[neighbor] = [
            item for item in self.graph[neighbor] if not (isinstance(item, dict) and self.current_node in item)
        ]
        print(f"Removed edge between {neighbor} and {self.current_node}.")

    def get_neighbors(self):
        neighboring_nodes = self.graph[self.current_node]
        return [list(n.keys())[0] for n in neighboring_nodes]

    def get_unvisited_nodes(self, nodes):
        return [item for item in nodes if item not in self.previous_path]
