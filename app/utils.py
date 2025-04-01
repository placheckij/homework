import logging
import os
import re
from pathlib import Path

LOG = logging.getLogger(__name__)


def get_version_from_pyproject():
    """Extract the version from pyproject.toml file."""
    try:
        # Get the project root directory
        project_root = Path(__file__).parent.parent
        pyproject_path = project_root / "pyproject.toml"

        # Check if the file exists
        if not pyproject_path.exists():
            LOG.warning(f"pyproject.toml not found at {pyproject_path}")
            return os.environ.get("MAIN_BACKEND_VERSION", "unknown")

        # Read the pyproject.toml file
        with open(pyproject_path, "r") as f:
            content = f.read()

        # Extract the version using regex
        version_match = re.search(r'^version\s*=\s*"([^"]+)"', content, re.MULTILINE)
        if version_match:
            version = version_match.group(1)
            return version
        else:
            LOG.warning("Version not found in pyproject.toml")
            return os.environ.get("MAIN_BACKEND_VERSION", "unknown")

    except Exception as e:
        LOG.error(f"Error reading version from pyproject.toml: {e}")
        return os.environ.get("MAIN_BACKEND_VERSION", "unknown")
