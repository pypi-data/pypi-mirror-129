# HBSpark
This project package is meant to be an interface between Hbase and spark that moves information directly from the thrift api to spark rdd.

NOTE: THIS PACKAGE IS UNDER HEAVY DEVELOPEMENT AND IS NOT MATURE IN ANY MEANS. BUGS AND CHANGES TO THE API SHOULD BE EXPECTED.

## Developement environment:
The current developement environment is as follows:
- python 3.6.9
- happybase 1.2.0
- pyspark 3.2.0

The target development environment is as follows:
- python 2.7.5
- happybase 1.2.0
- (spark) 2.2.0.cloudera1

Currently, dependency requirements through the package may be inconsistent. If issues persist, please emulate the developement environment provided above.

## Packaging:
This package has been created following the `https://packaging.python.org/tutorials/packaging-projects/` tutorial.
- pyproject.toml:
    - Determines dependencies for PIP
- setup.cfg:
    - Static configuration for setuptools (packagemanagement)

## Installation:
In order to install the package, pip can be used:
```
pip install hbspark
```

## Documentation
And for usage documentation, please refer to the [readthedocs](https://hbspark.readthedocs.io/en/latest/) page which includes an in depth [API](https://hbspark.readthedocs.io/en/latest/api_documentation.html).