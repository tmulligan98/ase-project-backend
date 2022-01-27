from pydantic import BaseModel
from fastapi import APIRouter, status, Response
from backend.utils import (
    get_tomtom_traffic_flow,
    TrafficFlowModel,
    ErrorModel,
    TrafficSources,
)

router = APIRouter()


class TrafficFlowInputModel(BaseModel):
    lat: int
    long: int
    zoom: int
    api_source: TrafficSources


@router.post("/traffic_flow", response_model=TrafficFlowModel)
async def post_traffic_flow(
    body: TrafficFlowInputModel, response: Response
) -> TrafficFlowModel:
    """
    Route to accept body specifying location and zoom of location,
    as well as the source of the traffic flow information
    """
    try:
        # Depending on source specified...
        if body.source == "tomtom":
            res = get_tomtom_traffic_flow(body.lat, body.long, body.zoom)
        return res
    except Exception:  # Should probably do proper error handling...
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return ErrorModel(message="Error", code=500)
