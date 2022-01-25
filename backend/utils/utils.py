from requests import get
import json
from backend.utils import SETTINGS
from .models import TrafficFlowModel
from .endpoints import TOMTOM_TRAFFIC_FLOW


def construct_tomtom_url(lat: float, long: float, zoom: float) -> str:
    """
    Utility function to construct a url for the tomtom traffic flow api

    Parameters
    ----------
    lat : float
        Latitude of location
    long : float
        longitude of location
    zoom : int
        Degree of zoom to location, effects number of streets concerned

    Returns
    -------
    url : str
    String url to be sent to tomtom
    """
    key = SETTINGS.tom_tom_access_key
    url = TOMTOM_TRAFFIC_FLOW + f"{zoom}/json?key={key}&point={lat},{long}"
    return url


# TODO: Specify pydantic basemodel
def get_tomtom_traffic_flow(lat: float, long: float, zoom: float) -> TrafficFlowModel:
    """
    Utility function to fetch traffic flow data
    from the tomtom traffic API

    Parameters
    ----------
    lat : float
        Latitude of location
    long : float
        longitude of location
    zoom : int
        Degree of zoom to location, effects number of streets concerned

    Returns
    -------
    Body of info
    """

    url = construct_tomtom_url(lat, long, zoom)
    body = get(url).content

    # Construct JSON body
    json_body = json.loads(body)
    print(json_body)
    # Populate the model with information
    model = TrafficFlowModel()

    # Return the model
    return model
