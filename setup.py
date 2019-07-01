"""Setup script for charybde."""
# -*- coding: utf-8 -*-
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

from setuptools import find_packages, setup

root = Path(__file__).parent

spec = spec_from_file_location("charybde", str(root / "charybde" / "__init__.py"))
charybde = module_from_spec(spec)
spec.loader.exec_module(charybde)  # type: ignore

long_description = "\n" + (root / "README.md").read_text(encoding="utf-8")

setup(
    name="charybde",
    version=".".join(map(str, charybde.__version__)),  # type: ignore
    description="Count syllables with neural networks.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="m09",
    author_email="142691+m09@users.noreply.github.com",
    python_requires=">=3.6.0",
    url="https://github.com/m09/charybde",
    packages=find_packages(exclude=("tests",)),
    install_requires=["beautifulsoup4", "requests", "tqdm"],
    include_package_data=True,
    entry_points={"console_scripts": ["charybde=charybde.__main__:main"]},
    license="Apache Software License",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Text Processing",
    ],
)
