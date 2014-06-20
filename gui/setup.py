import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="PlanarRad project GUI",
    version="0.1",
    author="Frédéric Boulé",
    author_email="frederic_boule@hotmail.fr",
    description=(
        "A GUI for DeconvolutionofSpecificInherentOpticalProperties(SIOPS)from hyperspectralremote sensing reflectance"),
    license="GNU General Public License Version 2 (GPLv2)",
    keywords="Second GUI PlanarRad",
    url="https://marrabld.github.io/planarradpy/",
    packages=['an_example_pypi_project', 'tests'],
    long_description=read('README'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
)
