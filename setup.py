from setuptools import setup, find_packages

setup(
    name="xautoflow",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.100.0",
        "uvicorn>=0.22.0",
        "sqlalchemy>=2.0.0",
        "psycopg2-binary>=2.9.6",
        "pydantic>=2.0.0",
        "httpx>=0.24.0",
        "langchain>=0.0.300",
        "vectorbt>=0.25.0",
        "pandas>=2.0.0",
        "pytest>=7.0.0",
    ],
) 