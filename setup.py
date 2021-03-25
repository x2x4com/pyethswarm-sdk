import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyethswarm",
    version="0.0.2",
    author="x2x4",
    author_email="x2x4com@gmail.com",
    description="A simple sdk for ethswarm",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/x2x4com/pyethswarm-sdk",
    project_urls={
        "Bug Tracker": "https://github.com/x2x4com/pyethswarm-sdk/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "."},
    packages=setuptools.find_packages(where="."),
    python_requires=">=3.6",
    install_requires=[
        "requests",
    ],
)
