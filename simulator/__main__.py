from simulator.graph_reader_yaml import GraphReaderYAML
from simulator.robot import Robot

if __name__ == "__main__":
    graph_reader = GraphReaderYAML()
    robot = Robot(
        graph_reader,
        graph_reader.read_base_graph(),
        start_node="E",
        target_node="B",
    )
    robot.check_next_nodes()
