from setuptools import setup, find_packages

setup(
    name="mul-bench",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click>=8.0",
        "pyyaml>=5.1",
        "pandas>=1.3",
        "numpy>=1.21",
        "biopython>=1.79",
        "matplotlib>=3.4",
        "seaborn>=0.11",
        "rich>=10.0",
    ],
    entry_points={
        "console_scripts": [
            "mul-bench=mul_bench.cli:main",
        ],
    },
    python_requires=">=3.8",
)
