from fastapi import APIRouter, status, Response
from backend.samples import SampleInputBody, SampleOutputBody

router = APIRouter()


@router.post("/sample_post", response_model=SampleOutputBody)
async def get_sample_message(
    body: SampleInputBody, response: Response
) -> SampleOutputBody:
    """ """
    try:
        return SampleOutputBody(message="Hello")
    except Exception:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return SampleOutputBody(message="Error")
