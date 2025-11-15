# Bricks

A PyBricks project for LEGO robotics programming with Python. This project provides custom robotics classes and utilities for building autonomous LEGO robots using the SPIKE Prime Hub.

## Features

- **ArtemisBase**: A custom `DriveBase` class that tracks robot position on the field and supports coordinate-based navigation
- **Geometry utilities**: Helper functions for working with coordinates and field positioning
- **Map utilities**: Tools for navigating predefined field maps
- **Testing framework**: Fake implementations for testing robot code without hardware
- **Jupyter notebook support**: Interactive development and experimentation

## Prerequisites

- [Pixi](https://pixi.sh/) - Fast package manager for conda environments
- A LEGO SPIKE Prime Hub or compatible hardware

## Setup

### 1. Install Pixi

If you don't have Pixi installed, install it using one of these methods:

**macOS/Linux:**
```bash
curl -fsSL https://pixi.sh/install.sh | bash
```

**Windows (PowerShell):**
```powershell
iwr -useb https://pixi.sh/install.ps1 | iex
```

For more installation options, see the [Pixi documentation](https://pixi.sh/latest/#installation).

### 2. Install Dependencies

Clone the repository and install dependencies:

```bash
cd bricks
pixi install
```

This will:
- Set up a Python 3.10+ environment
- Install all required dependencies (PyBricks, Jupyter, pytest, ruff, etc.)
- Configure the development environment

## Usage

### Running Code on the Hub

Connect your LEGO SPIKE Prime Hub via Bluetooth and run:

```bash
pixi run pbr
```

This uses `pybricksdev` to run code on your hub via Bluetooth Low Energy (BLE).

### Development Tasks

The project includes several convenient tasks:

```bash
# Run tests
pixi run test

# Format code with ruff
pixi run format

# Lint code with ruff
pixi run lint

# Fix linting issues automatically
pixi run lint --fix

# Launch Jupyter notebook
pixi run notebook
```

### Interactive Development

Start a Jupyter notebook session for interactive development:

```bash
pixi run notebook
```

This is useful for experimenting with robot behaviors and testing code snippets.

## Project Structure

```
bricks/
├── artemis_base.py              # Custom DriveBase with position tracking
├── artemis_config.py            # Robot configuration
├── geometry.py                  # Geometry and coordinate utilities
├── map.py                       # Field map utilities
├── fake.py                      # Mock implementations for testing
├── turntable.py                 # Turntable control utilities
├── brush_map_mineshaft_statue.py # Specific mission/map code
├── alpha.py                     # Additional robot utilities
├── execute.ipynb                # Execution notebook
├── pixi.toml                    # Pixi project configuration
└── pyproject.toml               # Python project and ruff configuration
```

## Development Workflow

1. **Write code**: Edit your Python files or use Jupyter notebooks
2. **Format**: Run `pixi run format` to auto-format your code
3. **Lint**: Run `pixi run lint` to check for issues
4. **Test**: Run `pixi run test` to execute tests
5. **Deploy**: Run `pixi run pbr` to upload and run on your hub

## Code Quality

This project uses [Ruff](https://docs.astral.sh/ruff/) for both formatting and linting:

- **Formatting**: Automatically formats code to maintain consistency
- **Linting**: Checks for common errors, style issues, and code quality problems
- **Configuration**: See `pyproject.toml` for Ruff settings

## Testing

Tests are written using pytest. Run the test suite with:

```bash
pixi run test
```

For testing without physical hardware, use the mock implementations in `fake.py`.

## Contributing

When contributing to this project:

1. Format your code: `pixi run format`
2. Fix linting issues: `pixi run lint --fix`
3. Run tests: `pixi run test`
4. Ensure all checks pass before committing

## Resources

- [PyBricks Documentation](https://pybricks.com/)
- [PyBricks API Reference](https://docs.pybricks.com/)
- [SPIKE Prime Hub](https://education.lego.com/en-us/products/lego-education-spike-prime-set/45678)
- [Pixi Documentation](https://pixi.sh/)

## License

This project is for educational and recreational use with LEGO robotics.
