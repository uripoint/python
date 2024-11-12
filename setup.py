from setuptools import setup, find_packages

setup(
    name="uripoint",
    version="1.9.6",
    description="A flexible Python library for endpoint management and URI processing",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="Tom Sapletta",
    author_email="info@softreck.dev",
    url="https://github.com/uripoint/python",
    packages=find_packages(exclude=['tests*']),
    install_requires=[
        'pyyaml>=6.0',
        'python-dotenv>=0.19.0',
        'ffmpeg-python>=0.2.0',
        'typing-extensions>=4.0.0',
        'colorlog>=6.7.0',
        'click>=8.0.0',
        'prometheus_client>=0.19.0',
        'fastapi>=0.104.1',
        'uvicorn>=0.24.0',
        'docker>=6.0.0',
        'requests>=2.28.0'
    ],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-cov>=4.0.0',
            'black>=23.0.0',
            'mypy>=1.9.6',
            'flake8>=6.0.0',
            'isort>=5.12.0',
            'coverage>=7.2.0'
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        "License :: OSI Approved :: Apache Software License",
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    python_requires='>=3.7',
    entry_points={
        'console_scripts': [
            'uripoint=uripoint.main:main',
        ],
    },
)
