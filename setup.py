from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="ssh-bruteforce-tool",
    version="1.0.0",
    author="Security Researcher",
    author_email="researcher@example.com",
    description="A Python SSH bruteforce tool for security testing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/example/ssh-bruteforce-tool",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Information Technology",
        "Topic :: Security",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "ssh-bruteforce=src.ssh_bruteforce:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["wordlists/*.txt", "docs/*.md"],
    },
)
