"""
Package setup
"""

from pathlib import Path

from setuptools import find_namespace_packages, setup

docs_packages = ["mkdocs==1.3.0", "mkdocstrings==0.18.1", "mkdocs-windmill==1.0.5"]

style_packages = ["black==22.3.0", "flake8==3.9.2", "isort==5.10.1"]

dev_packages = [
    "python-dotenv==1.0.0",
    "pytest==7.4.0",
    # "moto==4.1.12", # Uncomment if you need to mock AWS services
    "pytest-cov==4.1.0",
    "pytest-mock==3.11.1",
]

BASE_DIR = Path(__file__).parent
with open(Path(BASE_DIR, "requirements.txt"), "r") as file:
    required_packages = file.read().splitlines()

setup(
    name="src",
    version="0.0.1",
    description="Alarmbot",
    author="Joey Xiang",
    author_email="joey.xiang426@gmail.com",
    python_requires=">=3.8",
    packages=find_namespace_packages(),
    install_requires=required_packages,
    extras_require={
        "dev": dev_packages + docs_packages + style_packages,
        "docs": docs_packages,
    },
)