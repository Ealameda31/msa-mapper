import fiona
import geopandas as gpd
import io
import numpy as np
import os
from itertools import chain
from shapely.geometry import Point

abs_file_path = os.path.abspath(__file__)
dir_name = os.path.dirname(abs_file_path) + '/shapefiles/census/'


def _get_mapping_files(shp_str):
    """
    Given a string, this function will return the geographic information
    encoded in the shapefile containing the string value within the package's
    '/shapefiles/census/' directory.

    Args:
        shp_str (str): indicator to look for when parsing the shapefiles

    Returns:
        List [geopandas.geodataframe.GeoDataFrame, str]: list containing [0]
            the geodataframe associated with the shapefile, and [1] string
            representing the coordinate reference system used on that shapefile

    Raises:
        AssertionError: The string passed must designate a unique shapefile
            within the 'shapefiles/census/' package directory.
    """
    assert (isinstance(shp_str, str)), "Please ensure input is a string."
    file = [f for f in os.listdir(dir_name) if shp_str in f]
    assert (len(file) == 1), \
        "Shapefile with string designation not found or non-unique."
    shp = io.BytesIO(open(dir_name + file[0], 'rb').read())
    with fiona.BytesCollection(shp.read()) as src:
        crs = src.crs['init']
        gdf = gpd.GeoDataFrame.from_features(src, crs=crs)
    return gdf, crs


def map_census_locations(coords):
    """
    Given a list of longitude/latitude coordinate pairs or a single pair, this
    function will map the locations to the census-defined Metropolitan
    Statistical Area (MSA).

    Args:
        coords (tuple or list[tuple]): either a single coordinate pair
            or a list of longitude/latitude coordinates

    **Returns:**

    This function returns a geopandas.geodataframe.GeoDataFrame with the
    following columns

      | Column | Type | Description |
      | :----- | :--- | :---------- |
      | Coordinates | `shapely.geometry.Point`| coordinates \
          passed to the function as a shapely geometry |
      | MSA_Name | `str` | name given by the census to the MSA mapped to the \
          coordinate pair |
      | MSA_Fip_Code | `str` | code given by the census to describe the \
          coordinate pair area - useful when mapping to other sources |

    Raises:
        AssertionError: Coordinates must either be a list of tuples with two
            floats in each element or a single tuple with two floats.

    Examples:
        Function can be applied to a single coordinate pair or a list of
        coordinates and is robust to empty values:

        >>> from msa_mapper import map_census_locations
        >>> dc_lonlat = (-77.03637, 38.9072)
        >>> map_census_locations(dc_lonlat)
    """
    assert ((isinstance(coords, list)
             and all(x is None or type(x) == tuple for x in coords)
             and all(type(x) == float for x in
                     list(chain(*[[(m) for m in x]
                                  for x in coords if x is not None])))
             and all(x is None or len(x) == 2 for x in coords))
            or (isinstance(coords, tuple)
                and all(type(x) == float for x in coords)
                and len(coords) == 2)), \
                    ("Coordinates must either be a list of tuples with two"
                     + " floats in each element or a single tuple with two"
                     + " floats. Example [(0.2, 0.4), (0.5, 0.6)] or"
                     + " (0.2, 0.4).")

    metdiv_gdf = _get_mapping_files('metdiv')[0]
    cbsa_gdf, cbsa_crs = _get_mapping_files('cbsa')

    if type(coords) == list:
        lonlat_gdf_cbsa = (
            gpd.GeoDataFrame({"geometry": [Point(x) if x is not None else None
                                           for x in coords]},
                             crs=cbsa_crs)
        )
    else:
        lonlat_gdf_cbsa = (
            gpd.GeoDataFrame({"geometry": [Point(coords)]},
                             crs=cbsa_crs)
        )

    subset_metdiv = metdiv_gdf[["geometry", "NAME", "METDIVFP", "CBSAFP"]]
    subset_cbsa = cbsa_gdf[["geometry", "NAME", "CBSAFP"]]

    lonlat_metdiv_joined = (
        gpd.sjoin(lonlat_gdf_cbsa,
                  subset_metdiv,
                  how='left',
                  predicate='within')
        .drop("index_right", axis=1)
    )

    all_joined = (
        gpd.sjoin(lonlat_metdiv_joined,
                  subset_cbsa,
                  how='left',
                  predicate='within')
        .drop("index_right", axis=1)
    )

    all_joined["MSA_Name"] = (
        np.select(
            [(all_joined["NAME_left"].notnull()),
             (all_joined["NAME_left"].isnull())],
            [(all_joined["NAME_left"]),
             (all_joined["NAME_right"])])
    )

    all_joined["MSA_Fip_Code"] = (
        np.select(
            [(all_joined["METDIVFP"].notnull()),
             (all_joined["METDIVFP"].isnull())],
            [(all_joined["METDIVFP"]),
             (all_joined["CBSAFP_right"])])
    )

    all_joined = (
        all_joined[["geometry", "MSA_Name", "MSA_Fip_Code"]]
        .rename(columns={"geometry": "Coordinates"})
    )

    return all_joined
