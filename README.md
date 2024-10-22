# hslu-pren-simulator

## Requirements

- Python 3.9 or later
- Poetry 1.8 or later

## Installation

1. Clone the repository:
```bash
git clone https://github.com/ameyer3/hslu-pren-simulator.git
cd hslu-pren-simulator
```

2. Install dependencies using `poetry`:
```bash
poetry install
# or
make install
```

This will create a virtual environment and install all necessary dependencies defined in `pyproject.toml` file.

## Development
If you wish to contribute or modify the project, follow these steps:

1. Install `poetry`:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. Install the project in editable mode with development dependencies:
```bash
poetry install
# or
make install
```

3. Activate the virtual environment (Optionally):
```bash
poetry shell
```

4. Make your changes to the code and run tests:
```bash
poetry run pytest -v --cov-config .coveragerc --cov=simulator -l --tb=short --maxfail=1 tests/
poetry run coverage xml
poetry run coverage html
# or
make test
```

5. Lint and format code:
```bash
poetry run isort simulator/
poetry run black -l 79 simulator/
poetry run black -l 79 tests/
# or
make fmt
```

## Usage
Once installed, you can run the simulator using the following command:
```bash
poetry run python -m simulator
# or
make run
```

You can also run individual scripts or modules from within the `poetry` virtual environment:
```bash
poetry run python path/to/your_script.py
```

## Project Structure
```
hslu-pren-simulator/
│
├── simulator/           # Main simulator code
│   ├── __init__.py
│   ├── __main__.py      # Entrypoint
│   └── [Other modules]
│
├── tests/               # Test cases
│   └── test_simulator.py
│
├── pyproject.toml       # Poetry configuration
├── README.md            # Project readme (this file)
└── ...
```