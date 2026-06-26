import uuid

from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from .core.config import Settings

from app.features.auth.controller import router as auth_router

settings = Settings()
OTEL_EXPORTER_OTLP_ENDPOINT = settings.otel_exporter_otlp_endpoint


def setup_telemetry() -> None:
    resource = Resource.create(
        {
            "service.name": settings.app_name,
            "service.version": settings.app_version,
            "service.instance.id": str(uuid.uuid4()),
        }
    )

    provider = TracerProvider(resource=resource)

    exporter = OTLPSpanExporter(endpoint=OTEL_EXPORTER_OTLP_ENDPOINT, insecure=True)
    provider.add_span_processor(BatchSpanProcessor(exporter))
    trace.set_tracer_provider(provider)


setup_telemetry()

app = FastAPI(
    title=settings.app_name,
    description="A simple FastAPI application instrumented with OpenTelemetry for tracing.",
    version=settings.app_version,
)

FastAPIInstrumentor.instrument_app(app)

app.include_router(auth_router)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/ping")
def ping():
    tracer = trace.get_tracer(__name__)

    with tracer.start_as_current_span("ping-endpoint"):
        return {"message": "pong"}
