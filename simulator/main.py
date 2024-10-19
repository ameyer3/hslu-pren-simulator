from graph_reader_yaml import GraphReaderYAML
from robot import Robot
from path_calculator import PathCalculator

def run(robot):
    while not robot.has_reached_target():
        robot.check_next_nodes()
        robot.move_to_next_node()

if __name__ == '__main__':
    graph_reader = GraphReaderYAML()
    path_calculator = PathCalculator()
    robot = Robot(
        graph_reader=graph_reader,
        graph=graph_reader.read_base_graph(),
        start_node="E",
        target_node="C",
        path_calculator=path_calculator
        )
    run(robot)
