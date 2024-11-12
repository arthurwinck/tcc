from setuptools import setup  # type: ignore
from pathlib import Path


cwd = Path(__file__).parent
long_description = (cwd / "README.md").read_text()

setup(
    name="frontend",
    version="0.0.1",
    package_dir={"frontend": "dist"},
    package_data={"frontend": ["**/*.*"]},
    long_description=long_description,
    long_description_content_type="text/markdown",
)
