import heapq
from typing import Dict


class PathCalculator:
    path = []
    amount_of_no_change_in_graph = 0
    latest_graph = []

    def get_next_node(self, graph, start, target):
        if graph == self.latest_graph:
            self.amount_of_no_change_in_graph += 1
        else:
            print("Graph has changed, we need to calculate a new path.")
            self.latest_graph = graph
            self.amount_of_no_change_in_graph = 0
            distance, self.path = self._dijkstra(graph, start, target)
        print(f"Planned path is {self.path}")
        return self.path[self.amount_of_no_change_in_graph + 1]

    def _dijkstra(self, graph, start, target):
        distances = {node: float("inf") for node in graph}
        distances[start] = 0
        previous_nodes = {node: None for node in graph}

        # Priority queue to keep track of minimum distance nodes
        pq = [(0, start)]  # (distance, node)

        while pq:
            current_distance, current_node = heapq.heappop(pq)

            # If the current node is the target, stop and return the shortest path
            if current_node == target:
                path = []
                while current_node:
                    path.insert(0, current_node)
                    current_node = previous_nodes[current_node]
                return distances[target], path

            # If the current distance is greater than the already found shortest distance, skip
            if current_distance > distances[current_node]:
                continue

            # Iterate through the neighbors of the current node
            for neighbor_info in graph[current_node]:
                neighbor, weight = list(neighbor_info.items())[0]
                distance = current_distance + weight

                # If a shorter path is found
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous_nodes[neighbor] = current_node
                    heapq.heappush(pq, (distance, neighbor))
