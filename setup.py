from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="uripoint",
    version="0.0.1",
    author="Tom Sapletta",
    author_email="info@softreck.dev",
    description="A flexible URI point generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/uripoint-com/python",
    packages=find_packages(exclude=["tests*"]),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Video",
        "Topic :: System :: Systems Administration",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    include_package_data=True,
    package_data={
        "uripoint": [
            "config/*.json",
        ],
    },
    entry_points={
        "console_scripts": [
            "uripoint=uripoint.main:main",
        ],
    },
)
