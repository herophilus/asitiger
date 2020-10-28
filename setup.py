import setuptools

setuptools.setup(
    name="asitiger",
    version="0.0.1",
    author="Chili Johnson",
    author_email="chilijohnson@chilij.com",
    description="A thin library for controlling ASI Tiger Controllers",
    url="https://github.com/ChiliJohnson/asitiger",
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    install_requires=["pyserial>=3.4"],
    extras_require={
        "dev": ["black==19.10b0", "flake8-bugbear==19.8.0", "pre-commit>=2.7.1"]
    },
)
