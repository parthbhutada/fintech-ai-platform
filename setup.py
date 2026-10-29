from setuptools import setup, find_packages

setup(
    name="nexusfin-ai",
    version="1.0.0",
    author="FinTech AI Engineering Team",
    description="Enterprise AI Platform for Credit Scoring, Risk Management, Fraud Prevention & Decentralized Banking",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(where="."),
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.21.0",
        "pandas>=1.3.0",
        "scikit-learn>=1.0.0",
        "Flask>=2.0.0",
    ],
    entry_points={
        "console_scripts": [
            "nexusfin=src.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Topic :: Office/Business :: Financial :: Investment",
    ],
)
