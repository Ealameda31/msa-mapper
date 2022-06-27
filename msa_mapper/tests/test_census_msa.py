import pytest
from geopandas import GeoDataFrame
from msa_mapper.census_msa import map_census_locations


@pytest.mark.dependency(name="census_msa_single_sample")
def test_census_msa_single_sample():
    """
    Tests to see if census_msa's map_census_locations function is returning
    correct output for a single set of longitude/latitude coordinates
    """
    single_pair_coords = (-93.63, 41.59)
    lctn_single_gdf = map_census_locations(single_pair_coords)

    assert isinstance(lctn_single_gdf, GeoDataFrame),  \
        AssertionError('Single coordinate test output is not a GeoDataFrame')
    assert lctn_single_gdf.shape == (1, 3), \
        AssertionError('Single coordinate test output should return one row'
                       + ' and three columns')
    assert all(lctn_single_gdf.columns == ["Coordinates",
                                           "MSA_Name",
                                           "MSA_Fip_Code"]), \
        AssertionError('Single coordinate test columns'
                       + ' did not match names specified in order')
    assert lctn_single_gdf.MSA_Name[0].strip() == \
        'Des Moines-West Des Moines, IA', \
        AssertionError('Single coordinate test MSA value is not the'
                       + " expected one of 'Des Moines-West Des Moines, IA'")


@pytest.mark.dependency(name="census_msa_multi_sample")
def test_census_msa_multi_sample():
    """
    Tests to see if census_msa's map_census_locations function is returning
    correct output for multiple sets of longitude/latitude coordinates
    """
    multi_pair_coords = [
        (-93.63, 41.59),
        (-77.04, 38.91),
        (-66.05, 17.99),
        (-122.14, 37.44)
    ]
    lctn_multi_gdf = map_census_locations(multi_pair_coords)

    assert isinstance(lctn_multi_gdf, GeoDataFrame),  \
        AssertionError('Multiple coordinate test output is not a GeoDataFrame')
    assert lctn_multi_gdf.shape == (len(multi_pair_coords), 3), \
        AssertionError('Multiple coordinate test output should return same'
                       + ' number of rows as coords passed and three columns')
    assert all(lctn_multi_gdf.columns == ["Coordinates",
                                          "MSA_Name",
                                          "MSA_Fip_Code"]), \
        AssertionError('Multiple coordinate test columns'
                       + ' did not match names specified in order')
    assert all(lctn_multi_gdf.MSA_Name.values == [
        'Des Moines-West Des Moines, IA',
        'Washington-Arlington-Alexandria, DC-VA-MD-WV',
        'Guayama, PR',
        'San Jose-Sunnyvale-Santa Clara, CA']), \
        AssertionError('Multiple coordinate test MSA values'
                       + 'did not align with the coordinates specified')
