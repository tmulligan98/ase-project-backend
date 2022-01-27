from typing import Dict, Any
import requests
import json
from backend.utils import SETTINGS
from .models import TrafficFlowModel, StreetModel
from .endpoints import TOMTOM_TRAFFIC_FLOW


def parse_tom_tom_response(body: Dict[str, Any]) -> StreetModel:
    """
    Function to parse content from the TomTom Traffic
    flow reponse

    Parameters
    ----------
    body : dict
        Dictionary containing the reponse details from TomTom

    Returns
    -------
    model : StreetModel
    Basemodel containing the info we want
    """
    details = body["flowSegmentData"]
    speed = details["currentSpeed"]
    temp_coords = details["coordinates"]["coordinate"]

    coords = [(c["latitude"], c["longitude"]) for c in temp_coords]

    model = StreetModel(speed=speed, coords_of_street=coords)
    return model


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
    body = requests.get(url).content

    # Construct JSON body
    json_body = json.loads(body)
    # Populate the model with information
    model = parse_tom_tom_response(json_body)
    # Return the model
    return TrafficFlowModel(streets=[model])
