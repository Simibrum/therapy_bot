"""Configuration helper functions."""
import os


# Load the environment variables if working in weird environments
def load_from_env_file():
    """Load environment variables from a file."""
    # Load environment variables from project root .env file
    # Get the current file's directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Get the parent directory of the current file's directory
    parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
    grandparent_dir = os.path.abspath(os.path.join(parent_dir, os.pardir))
    # Set path of .env file
    env_path = os.path.join(grandparent_dir, ".env")
    try:
        # Load environment variables from .env file
        load_env_vars(env_path)
    except FileNotFoundError:
        pass


def load_env_vars(path):
    """Load environment variables from a file."""
    with open(path) as f:
        for line in f:
            if "=" in line and not line.startswith("#"):
                # Split the line into the variable name and value
                var, value = line.split("=")

                # Strip leading and trailing whitespace from the variable name and value
                var = var.strip()
                value = value.strip()

                if var and value:
                    # Set the environment variable
                    os.environ[var] = value


def read_version_from_file():
    """Read the version from a file."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Get the parent directory of the current file's directory
    parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
    # Set path of version file
    filename = os.path.join(parent_dir, "version.txt")
    with open(filename, "r") as file:
        # Read the first line and strip any newline characters or spaces
        version = file.readline().strip()
    return version
