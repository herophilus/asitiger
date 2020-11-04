import setuptools

with open("README.md", "r") as readme_file:
    long_description = readme_file.read()


setuptools.setup(
    name="asitiger",
    version="0.0.3",
    author="Chili Johnson",
    author_email="chilij@chilij.com",
    description="A thin Python interface for communicating with ASI Tiger Controllers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/System1Bio/asitiger",
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    install_requires=["pyserial>=3.0"],
    extras_require={
        "dev": ["black==19.10b0", "flake8-bugbear==19.8.0", "pre-commit>=2.7.1"]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
