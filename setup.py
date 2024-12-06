from setuptools import find_packages, setup

setup(
    name="KMG2D-Python",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
)
