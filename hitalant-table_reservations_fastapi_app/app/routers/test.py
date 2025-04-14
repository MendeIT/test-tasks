from fastapi import APIRouter


router_test = APIRouter(prefix="/api/v1/test", tags=["test"])


@router_test.get('/')
async def test():
    return {'message': 'OK'}
