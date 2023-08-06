import os
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

ver = os.environ.get('VERSION')

setuptools.setup(
    name="anko-sdk",
    version=ver,
    author="Anglo Korean",
    author_email="hello@anglo-korean.com",
    description="Python SDK for https://anko-investor.com market forecasts. Signup today!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/anglo-korean/anko-python-sdk",
    project_urls={
        "Bug Tracker": "https://github.com/anglo-korean/anko-python-sdk/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=["anko", "anko.proto"],
    python_requires=">=3.6",
    install_requires=[
        "grpcio",
    ],
)
