import fastapi
from fastapi import responses

router = fastapi.APIRouter()


@router.get('/', include_in_schema=False)
async def index():
    return responses.FileResponse('auth_service/static/index.html')
