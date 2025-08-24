import random
import uvicorn
import prometheus_client
from fastapi import FastAPI, APIRouter, Response
from fastapi.middleware.cors import CORSMiddleware
from time import time

app = FastAPI(debug=True)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)
router = APIRouter()

request_count = prometheus_client.Counter(
    'requests_total', 'Requests count', ['method', 'endpoint']
)

request_latency = prometheus_client.Histogram(
    'requests_latency', 'Request duration', ['method', 'endpoint']
)

@app.middleware("http")
async def middle_func(request, call_next):
    start_time = time()
    response = await call_next(request)
    duration = time() - start_time
    method = request.method
    endpoint = request.url.path
    print(f"Request: {method} {endpoint} completed in {duration}s")
    request_count.labels(method=method, endpoint=endpoint).inc()
    request_latency.labels(method=method, endpoint=endpoint).observe(duration)
    return response

@app.get("/metrics")
async def metrics():
    return Response(
        prometheus_client.generate_latest(), 
        media_type="text/plain"
    )

# Routes
@router.get("/")
async def root():
    return {"Hello": f"This is calling from Nandini's server {random.randint(1,100)}"}

app.include_router(router=router)

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=5000)