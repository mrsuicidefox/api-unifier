from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="api-unifier",
    version="1.0.0",
    author="API Unifier Contributors",
    author_email="contributors@api-unifier.dev",
    description="Make all APIs work the same way - Universal wrapper for REST, GraphQL, and SOAP",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/libra-ouros/api-unifier",
    py_modules=["api_unifier"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.25.0",
    ],
    keywords="api rest graphql soap wrapper universal normalization",
    project_urls={
        "Bug Reports": "https://github.com/libra-ouros/api-unifier/issues",
        "Source": "https://github.com/libra-ouros/api-unifier",
        "Documentation": "https://github.com/libra-ouros/api-unifier/blob/main/README.md",
    },
)
