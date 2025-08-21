from fastapi import FastAPI, APIRouter

app = FastAPI()
router = APIRouter()

@router.post("/")
def root(name: str):
    return {"Hello": f"Your name is {name}"}

app.include_router(router=router)