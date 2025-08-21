from fastapi import FastAPI, APIRouter

app = FastAPI()
router = APIRouter()

@router.get("/")
def root():
    return {"Hello": "This is calling from Nandini's server"}

app.include_router(router=router)