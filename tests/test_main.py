from simulator.graph_reader_yaml import GraphReaderYAML
from simulator.__main__ import run
from simulator.path_calculator import PathCalculator
from simulator.robot import Robot


def test_main_with_base_config():
    # Arrange
    graph_reader = GraphReaderYAML()
    path_calculator = PathCalculator()
    robot = Robot(
        graph_reader=graph_reader,
        graph=graph_reader.read_base_graph(),
        start_node="E",
        target_node="C",
        path_calculator=path_calculator,
    )

    # Act
    run(robot)

    # Assert
    assert robot.current_node == robot.target_node
    assert "F" not in robot.graph
