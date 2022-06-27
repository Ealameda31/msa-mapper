# msa-mapper
Python library which helps users geocode locations and map longitude/latitude coordinates to the Metropolitan Statistical Areas (MSAs) defined by the Census Bureau.

-------------------
## Table of Contents
- [Requirements](#requirements)
- [Installation](#installation)
- [Documentation](#documentation)
- [Manual Dependencies](#manual-dependencies)
- [Contact](#contact)

## Requirements
The Python version used for development is `3.10.4`. Below are a series of steps to follow before installation:
  1) Create a Python virtual environment where the library can be installed

  2) Clone this repository within a computer directory (folder) of your choice (please ensure Git is installed and an SSH key is specified for your profile):
      ```bash
        git clone git@github.com:Ealameda31/msa-mapper.git
      ```

  3) Initialize Git LFS and pull the files the library needs for certain functions:
        ```bash
          git lfs install
          git lfs pull
        ```

## Installation
After activating a Python virtual environment, users should navigate to the repository contents (i.e., `cd msa-mapper/`) and run the following command:
```bash
  python setup.py bdist_wheel 
```

This should create a `dist` folder within your directory containing the wheel file. Then, the library can be installed within your environment by running the command below:
```bash
  pip install dist/*
```

If users are experiencing issues with geospatial packages, download them from [Christoph Gohlke's Binaries](https://www.lfd.uci.edu/~gohlke/).  Download and install the wheel file that corresponds to the environment's Python version (i.e., Python `3.10.4` = `cp310`). Usually problems resolve after manually installing `GDAL` and `Fiona`.

## Documentation
Library structure, function documentation, and examples to follow can be found on [this webpage](https://ealameda31.github.io/msa-mapper/).

## Manual Dependencies
Shapefiles are manually uploaded and are located within the internal directory of the library. These file are stored in Git LFS to avoid unnecessary data downloads. They are updated on an infrequent basis (every 10 years) but finding a way to cross-reference the shapefiles programmatically would be ideal.
s
## Contact
Feel free to create an issue within this GitHub repository if a bug is found or for additional enhancements. The developers will typically respond within 48 hours.

For additional questions and/or use-cases, please contact Enrique M. Alameda-Basora (emalameda96@gmail.com).
