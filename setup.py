import setuptools


with open("README.md") as fp:
    long_description = fp.read()


setuptools.setup(
    name="deepcell-evaluator",
    version="0.0.1",

    description="Api to solve Deepcell Challange using GraphQl and REST APIs, Python CDK for AWS infra and GitHub for CI/CD",
    long_description=long_description,
    long_description_content_type="text/markdown",

    author="Rafael Gonçalves",

    package_dir={"": "deepcell_evaluator"},
    packages=setuptools.find_packages(where="deepcell_evaluator"),

    install_requires=[
        "aws-cdk.core",
    ],

    python_requires=">=3.8",

    classifiers=[
        "Programming Language :: Python :: 3.8",

        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",

        "Typing :: Typed",
    ],
)