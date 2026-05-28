from setuptools import setup, find_packages

setup(
    name="owura",
    version="1.0.0",
    description="AI Coding Agent for Mobile Terminal",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="OWURA",
    python_requires=">=3.8",
    packages=find_packages(),
    install_requires=[
        "rich>=13.0.0",
    ],
    entry_points={
        "console_scripts": [
            "owura=owura.app:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries",
    ],
)
