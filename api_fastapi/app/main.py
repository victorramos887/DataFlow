from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.asyncio import AsyncioInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

import os
import uuid

OTEL_EXPORTER_OTLP_ENDPOINT = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT", "http://otel-lgtm:4317")

def setup_telemetry() -> None:
    resource = Resource.create(
        {
            "service.name": "fastapi-service",
            "service.version": "1.0.0",
            "service.instance.id": str(uuid.uuid4()),
        }
    )
    
    provider = TracerProvider(resource=resource)
    
    exporter = OTLPSpanExporter(endpoint=OTEL_EXPORTER_OTLP_ENDPOINT, insecure=True)
    provider.add_span_processor(BatchSpanProcessor(exporter))
    trace.set_tracer_provider(provider)
    
setup_telemetry()

app = FastAPI(
    title="FastAPI with OpenTelemetry",
    description="A simple FastAPI application instrumented with OpenTelemetry for tracing.",
    version="1.0.0",
)

FastAPIInstrumentor.instrument_app(app)

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/ping")
def ping():
    tracer = trace.get_tracer(__name__)
    
    with tracer.start_as_current_span("ping-endpoint"):
        return {"message": "pong"}
