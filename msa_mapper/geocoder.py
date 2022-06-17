import geocoder
import time
from msa_mapper.utils import state_mapping


def _obtain_attributes(resp):
    """
    Given a response from the ArcGIS geocoding API, this function returns the
    address and longitude/latitude coordinate pair in a list.

    Args:
        resp (geocoder.arcgis.ArcgisResult): result obtained from a request
            made to the arcgis geocoding API

    Returns:
        list[str, tuple]: list containing [0] the official address and [1]
            location coordinates for the result passed to the function
    """
    lat, lon = resp.latlng
    return [resp.address,
            tuple([lon, lat])]


def get_geoinfo(address, city=None, state=None):
    """
    Given a street address, city, and state, this function will
    call the ArcGIS API and geocode the location - returning the full
    address and the longitude/latitude coordinate pair for the mapped location.
    Function will automatically convert all parameters to strings.

    Args:
        address (object): street address for the location to geocode
        city (object): the U.S. city the location is located in
        state (object): the U.S. state the location is located in

    Returns:
        list[str, tuple]: list containing [0] the official address obtained
            from the ArcGIS API, and [1] the longitute/latitude coordinate pair

    Example:
        To geocode a single street address:

        >>> from msa_mapper import get_geoinfo
        >>> get_geoinfo('801 Grand Ave', 'Des Moines')
        Out[1]: ['801 Grand Ave, Des Moines, IA 50309',
        ...      (-93.6285390023275, 41.58744200206709)]

        To geocode multiple addresses stored in a pandas DataFrame
        (`addresses_pdf`) with columns for each parameter
        (`Address`, `City`, `State`), we recommend installing and importing
        `pandarallel` to parallelize the apply function:

        >>> import multiprocessing
        >>> from pandarallel import pandarallel

        >>> num_cores = multiprocessing.cpu_count()
        >>> pandarallel.initialize(progress_bar=True,
        ...                        nb_workers=(num_cores - 1))

        >>> def func_name(x):
        ...     from msa_mapper import get_geoinfo
        ...     return get_geoinfo(x.Address, x.City, x.State)

        >>> res = (
        ...       addresses_pdf
        ...       .parallel_apply(func_name, axis=1)
        ... )
        >>> addresses = res.str[0].tolist()
        >>> coords = res.str[1].tolist()
    """
    if address:
        address = (
            str(address)
            .split('-')[-1]
            .split('&')[-1]
            .split(';')[-1]
            .strip()
            .encode('ascii', errors='ignore')
            .decode()
        )

    city_filtered = str(city).lower().strip()
    if city and city_filtered not in ('vr', 'various'):
        city = city_filtered.encode('ascii', errors='ignore').decode()
    else:
        city = None

    state_filtered = str(state).upper().strip()
    if state and state_filtered in state_mapping().keys():
        state = (
            state_filtered
            .encode('ascii', errors='ignore').decode()
        )
    else:
        state = None

    search = ', '.join(id for id in [address, city, state] if id)
    response = geocoder.arcgis(search, timeout=30)

    if response.ok:
        return _obtain_attributes(response)
    else:
        time.sleep(3)
        response = geocoder.arcgis(search, timeout=30)
        if response.ok:
            return _obtain_attributes(response)
        else:
            return None
