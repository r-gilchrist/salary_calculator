from setuptools import setup

setup(
    name="salary-calc",
    version="0.1.1",
    author="Ryan Gilchrist",
    author_email="ryangilchrist92@outlook.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Topic :: Personal Finance"
    ],
    description="Tools for calculating personal salary",
    include_package_data=True,
    install_requires=[
        "marshmallow==3.18.0",
        "marshmallow_enum==1.5.1"
    ],
    packages=[
        "salary_calculator.models",
        "salary_calculator.helpers",
        "salary_calculator.endpoints",
        "salary_calculator.data"
    ],
    python_requires=">=3.9"
)
