from setuptools import setup, find_packages

VERSION = '1.0.0'
DESCRIPTION = 'A package for converting DBLP data into JSON format with varying capacities for benchmarking software performance.'

setup(
    name="BD_Dev_Benchmark",
    version=VERSION,  
    author="Huangjing LEI and Yuan YAN", 
    author_email="huangjingleifr@gmail.com, yuan36803@gmail.com",
    description=DESCRIPTION,
    long_description=open("README.md").read(),  
    long_description_content_type="text/markdown",
    url="https://github.com/Bonjoureloi/BD-Benchmark-Base-en-sparql", 
    packages=find_packages(), 
    keywords=['python', 'DBLP', 'Benchmark', 'Base de donnees'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License", 
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
