import setuptools

setuptools.setup(
    name="LqsDatabase",
    version="1.0.0",
    author="Omar Elsayd",
    email="omar_2546@hotmail.com",
    discription="LQS database models and api",
    packages=setuptools.find_packages(),
    classifiers=["Programming Language :: Python :: 3.11"],
    install_requires=[
        "sqlalchemy",
        "fastapi",
        "uvicorn",
        "alembic",
        ]
    )