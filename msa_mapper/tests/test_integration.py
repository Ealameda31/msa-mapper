import pytest
from msa_mapper.census_msa import map_census_locations
from msa_mapper.geocoder import get_geoinfo


@pytest.mark.dependency(name="integration_sample",
                        depends=["geocoder_sample",
                                 "census_msa_single_sample"],
                        scope='session')
def test_integration_sample():
    """
    Tests to see if the geocoder and MSA mapper can be integrated and the
    correct output is returned
    """
    coords = get_geoinfo(address='Mammoth Cave', city='Kentucky')[1]
    msa_gdf = map_census_locations(coords)
    assert msa_gdf.MSA_Name[0].strip() == 'Bowling Green, KY', \
        AssertionError('Integration test MSA value is not the'
                       + " expected one of 'Bowling Green, KY'")
