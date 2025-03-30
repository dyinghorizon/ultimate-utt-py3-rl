from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ultimate-ttt-rl",
    version="0.1.0",
    author="dyinghorizon",
    author_email="",
    description="Reinforcement Learning based Ultimate Tic Tac Toe player (Python 3)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dyinghorizon/ultimate-utt-py3-rl",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "numpy",
        "matplotlib",
        "pandas",
        "keras",
        "tensorflow",
    ],
    entry_points={
        "console_scripts": [
            "ultimate-ttt-train=ultimate_ttt_rl.scripts.test_scripts:playUltimateAndPlotResults",
        ],
    },
)
