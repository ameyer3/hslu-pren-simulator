from simulator.graph_reader_yaml import GraphReaderYAML
from simulator.path_calculator import PathCalculator
from simulator.robot import Robot


def run(robot):
    while not robot.has_reached_target():
        neighbors = robot.check_next_nodes()
        robot.move_to_next_node(neighbors)
    print(f"Reached the target {robot.target_node} via {robot.previous_path}")

if __name__ == "__main__":
    graph_reader = GraphReaderYAML()
    path_calculator = PathCalculator()
    robot = Robot(
        graph_reader=graph_reader,
        graph=graph_reader.read_base_graph(),
        start_node="E",
        target_node="C",
        path_calculator=path_calculator,
    )
    run(robot)
