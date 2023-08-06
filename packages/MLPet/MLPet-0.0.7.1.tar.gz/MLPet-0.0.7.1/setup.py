import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="MLPet",
    version="0.0.7.1",
    author="Flavia Dias Casagrande",
    author_email="flavia.dias.casagrande@akerbp.com",
    description="Package to prepare well log data for ML projects.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/akerbp/mlpet/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
    install_requires=[
        "cognite-sdk>=2.31.0",
        "imbalanced-learn>=0.8.0",
        "joblib==1.0.1",
        "numpy>=1.19.5",
        "pandas>=1.3.2",
        "scikit-learn>=0.24.2",
        "scipy>=1.7.1",
        "pyyaml"
    ]

)
