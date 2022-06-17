from math import isclose
from msa_mapper.geocoder import get_geoinfo


def test_sample():
    """
    Tests to see if geocoder's get_geoinfo function is returning correct output
    """
    addrss, coords = get_geoinfo('801 Grand Ave, Des Moines, Iowa, 50309')

    if not isinstance(addrss, str):
        raise TypeError('Address returned by geocoder is not a string')
    if not (isinstance(coords, tuple) and len(coords) == 2):
        raise ValueError('Coordinates were not returned as a two-length tuple')

    if addrss.strip() != '801 Grand Ave, Des Moines, Iowa, 50309':
        raise ValueError('Test case address was not expected output')
    assert (isclose(coords[0], -93.63, abs_tol=0.01)
            and isclose(coords[1], 41.59, abs_tol=0.01)), \
        "Test case coordinates did not match expected values"
