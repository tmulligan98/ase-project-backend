from pydantic import BaseModel, Field
from fastapi import APIRouter, status, Response
from backend.external_apis import (
    get_tomtom_traffic_flow,
    TrafficFlowModel,
    TrafficSources,
)
from utils import ErrorModel

router = APIRouter()


class TrafficFlowInputModel(BaseModel):
    lat: float
    long: float
    zoom: int = Field(gt=5, lt=20)
    api_source: TrafficSources


@router.post("/traffic_flow", response_model=TrafficFlowModel)
def post_traffic_flow(
    body: TrafficFlowInputModel, response: Response
) -> TrafficFlowModel:
    """
    Route to accept body specifying location and zoom of location,
    as well as the source of the traffic flow information
    """
    try:
        # Depending on source specified...
        if body.api_source == TrafficSources.TOMTOM:
            res = get_tomtom_traffic_flow(body.lat, body.long, body.zoom)
        response.status_code = status.HTTP_200_OK
        return res
    except Exception:  # Should probably do proper error handling...
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return ErrorModel(message="Error", code=500)
