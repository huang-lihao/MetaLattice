"""A setuptools based setup module.
See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""
import sys

sys.path.insert(0, ".")  # to import versioneer

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import pathlib
import versioneer

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="metalattice",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="A python FEM package to model lattice metamaterials.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/huang-lihao/MetaLattice",
    author="Lihao HUANG",
    author_email="huang-lihao@outlook.com",
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    keywords="cosserat, micropolar, metamaterial, lattice",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    project_urls={
        "Bug Tracker": "https://github.com/huang-lihao/MetaLattice/issues",
        "Source": "https://github.com/huang-lihao/MetaLattice/",
    },
)
