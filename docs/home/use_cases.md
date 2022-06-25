# Use-Cases
-----------
The Python library, `msa_mapper`, contains two modules:

  1. [Geographic Decoder](/modules/geocoder)
  2. [Census MSA Mapping](/modules/census_msa)

These modules each serve a specific purpose but can be combined to provide geopolitical regions for any location. To accomplish this, users can follow the workflow below:

``` mermaid
    graph LR
    A[Obtain addresses] --> B[Acquire lat/lon coords via Geocoder];
    B --> C[Map coords to regions via Census mapper];
```

Simple Python code is provided below to reproduce this workflow:

```py
# Importing libraries
import pandas as pd
from msa_mapper import (
    get_geoinfo,
    map_census_locations
)
```

```py
# Reading CSV file with addresses
addresses_pdf = pd.read_csv('addresses.csv')
```

```py
# Acquiring lat/lon coords using an assumed "Address" column
addresses_pdf['coords'] = (
    addresses_pdf.apply(lambda x: get_geoinfo(x.Address)[1], axis=1)
)
```

```py
# Mapping coordinates to regions
addresses_pdf['MSA_regions'] = (
    map_census_locations(addresses_pdf.coords.tolist()).MSA_Name.values
)
```