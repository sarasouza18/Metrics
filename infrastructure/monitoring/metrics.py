# infrastructure/monitoring/metrics.py
from prometheus_client import multiprocess, CollectorRegistry, Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Response

registry = CollectorRegistry()

# Defina suas métricas
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP Requests',
    ['method', 'endpoint', 'http_status'],
    registry=registry
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency',
    ['method', 'endpoint'],
    registry=registry
)

def monitor_request(request, response):
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        http_status=response.status_code
    ).inc()

def metrics_endpoint():
    return Response(
        generate_latest(registry),
        headers={'Content-Type': CONTENT_TYPE_LATEST}
    )