from math import isclose
from msa_mapper.geocoder import get_geoinfo


def test_geocoder_sample():
    """
    Tests to see if geocoder's get_geoinfo function is returning correct output
    """
    addrss, coords = get_geoinfo('801 Grand Ave, Des Moines, Iowa, 50309')

    assert isinstance(addrss, str),  \
        AssertionError('Address returned by geocoder is not a string')
    assert (isinstance(coords, tuple) and len(coords) == 2), \
        AssertionError('Coordinates were not returned as a two-length tuple')

    assert addrss.strip() == '801 Grand Ave, Des Moines, Iowa, 50309', \
        AssertionError('Test case address was not expected output')
    assert (isclose(coords[0], -93.63, abs_tol=0.01)
            and isclose(coords[1], 41.59, abs_tol=0.01)), \
        AssertionError("Test case coordinates did not match expected values")
