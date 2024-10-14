import pygame
import sys


class Gui:
    def __init__(self, graph: dict):
        self.graph = graph

        # Initialize Pygame
        pygame.init()

        # Set up display
        self.WIDTH, self.HEIGHT = 600, 600
        self.WINDOW = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Graph with 8 nodes")

        self.font = pygame.font.Font(None, 30)

        self.nodes_coordinates = {
            'E': (300, 100),
            'F': (127, 200),
            'G': (242, 200),
            'D': (473, 200),
            'H': (300, 300),
            'A': (127, 400),
            'B': (300, 500),
            'C': (473, 400)
        }

    def main_loop(self):
        running = True
        while running:
            self.WINDOW.fill("white")

            # Draw nodes
            for node, edges in self.graph.items():
                coordinates = self.nodes_coordinates[node]
                pygame.draw.circle(self.WINDOW, "black",
                                   coordinates, 25)

                for edge in edges:
                    end_pos = self.nodes_coordinates[edge[0]]
                    pygame.draw.line(self.WINDOW, "black",
                                     coordinates, end_pos, 10)

            # Render text on nodes
            for node in self.graph:
                coordinates = self.nodes_coordinates[node]
                text_surface = self.font.render(node, True, "white")
                self.WINDOW.blit(
                    text_surface, (coordinates[0]-7.5, coordinates[1]-10))

            pygame.display.flip()

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        print("Key A has been pressed")

        # Clean up
        pygame.quit()
        sys.exit()


if __name__ == "__main__":

    # Define a weighted graph using an adjacency list representation
    graph = {
        'A': [('B', 10), ('F', 10), ('G', 12), ('H', 10)],
        'B': [('A', 10), ('C', 10), ('H', 10)],
        'C': [('B', 10), ('D', 10), ('H', 10)],
        'D': [('C', 10), ('E', 10), ('G', 12), ('H', 10)],
        'E': [('D', 10), ('F', 10), ('G', 6)],
        'F': [('A', 10), ('E', 10), ('G', 6)],
        'G': [('A', 12), ('D', 12), ('E', 6), ('F', 6), ('H', 6)],
        'H': [('A', 10), ('B', 10), ('C', 10), ('D', 10), ('G', 6)],
    }

    game = Gui(graph)
    game.main_loop()
