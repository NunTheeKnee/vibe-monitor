import random
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)
router = APIRouter()

@router.get("/")
def root():
    return {"Hello": f"This is calling from Nandini's server {random.randint(1,100)}"}

app.include_router(router=router)

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=5000)