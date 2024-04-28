from fastapi import APIRouter

router = APIRouter(prefix="/index")


@router.get("")
def read_root():
    return {"Hello": "World"}
