import random
import uvicorn
import prometheus_client
from fastapi import FastAPI, APIRouter, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from time import time

from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor

resource = Resource.create({
    "service.name": "vibe-monitor-api",
    "service.version": "0.1.0",
    "deployment.environment": "local",
})

provider = TracerProvider(resource=resource)
exporter = OTLPSpanExporter(endpoint="http://jaeger:4317", insecure=True)
processor = BatchSpanProcessor(exporter)
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

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
async def middle_func(request: Request, call_next):
    start_time = time()
    response = await call_next(request)
    duration = time() - start_time
    method = request.method
    endpoint = request.url.path
    span = trace.get_current_span()
    span_context = span.get_span_context()
    if span_context.is_valid:
        trace_id = format(span_context.trace_id, "032x")
        span_id = format(span_context.span_id, "016x")
        print(f"Request: {method} {endpoint} completed in {duration:.4f}s | trace_id={trace_id} span_id={span_id}")
    else:
        print(f"Request: {method} {endpoint} completed in {duration:.4f}s | no valid trace")
    request_count.labels(method=method, endpoint=endpoint).inc()
    request_latency.labels(method=method, endpoint=endpoint).observe(duration)
    return response

@app.get("/metrics")
async def metrics():
    return Response(
        prometheus_client.generate_latest(), 
        media_type="text/plain"
    )

@router.get("/")
async def root():
    return {"Hello": f"This is calling from Nandini's server {random.randint(1,100)}"}

app.include_router(router=router)

FastAPIInstrumentor.instrument_app(app)
RequestsInstrumentor().instrument()

if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=5000)
