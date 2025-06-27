"""
Monitoring configuration for the Media Authentication System.
"""

import time
from typing import Dict, Any
from prometheus_client import Counter, Histogram, Gauge, Summary
import structlog

logger = structlog.get_logger()

# Prometheus metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency',
    ['method', 'endpoint']
)

MODEL_INFERENCE_TIME = Histogram(
    'model_inference_duration_seconds',
    'Model inference time',
    ['model_type', 'file_type']
)

MODEL_PREDICTIONS = Counter(
    'model_predictions_total',
    'Total model predictions',
    ['model_type', 'prediction', 'confidence_level']
)

FILE_UPLOADS = Counter(
    'file_uploads_total',
    'Total file uploads',
    ['file_type', 'status']
)

ACTIVE_CONNECTIONS = Gauge(
    'active_connections',
    'Number of active connections'
)

SYSTEM_MEMORY_USAGE = Gauge(
    'system_memory_bytes',
    'System memory usage in bytes'
)

SYSTEM_CPU_USAGE = Gauge(
    'system_cpu_percent',
    'System CPU usage percentage'
)

UPLOAD_FILE_SIZE = Histogram(
    'upload_file_size_bytes',
    'Upload file size distribution',
    ['file_type']
)

PROCESSING_QUEUE_SIZE = Gauge(
    'processing_queue_size',
    'Number of files in processing queue'
)


class MetricsMiddleware:
    """Middleware for collecting HTTP metrics."""
    
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            start_time = time.time()
            method = scope["method"]
            path = scope["path"]
            
            # Track active connections
            ACTIVE_CONNECTIONS.inc()
            
            response_status = None
            
            async def send_wrapper(message):
                nonlocal response_status
                if message["type"] == "http.response.start":
                    response_status = message["status"]
                await send(message)
            
            try:
                await self.app(scope, receive, send_wrapper)
            finally:
                # Record metrics
                duration = time.time() - start_time
                REQUEST_LATENCY.labels(method=method, endpoint=path).observe(duration)
                
                if response_status:
                    REQUEST_COUNT.labels(
                        method=method, 
                        endpoint=path, 
                        status=response_status
                    ).inc()
                
                ACTIVE_CONNECTIONS.dec()
        else:
            await self.app(scope, receive, send)


class ModelMetrics:
    """Metrics collection for model operations."""
    
    @staticmethod
    def record_inference_time(model_type: str, file_type: str, duration: float):
        """Record model inference time."""
        MODEL_INFERENCE_TIME.labels(
            model_type=model_type, 
            file_type=file_type
        ).observe(duration)
    
    @staticmethod
    def record_prediction(model_type: str, prediction: str, confidence: float):
        """Record model prediction."""
        confidence_level = "high" if confidence > 0.8 else "medium" if confidence > 0.6 else "low"
        MODEL_PREDICTIONS.labels(
            model_type=model_type,
            prediction=prediction,
            confidence_level=confidence_level
        ).inc()
    
    @staticmethod
    def record_file_upload(file_type: str, status: str):
        """Record file upload."""
        FILE_UPLOADS.labels(file_type=file_type, status=status).inc()
    
    @staticmethod
    def record_file_size(file_type: str, size_bytes: int):
        """Record file size."""
        UPLOAD_FILE_SIZE.labels(file_type=file_type).observe(size_bytes)


class SystemMetrics:
    """System-level metrics collection."""
    
    @staticmethod
    def update_memory_usage(bytes_used: int):
        """Update memory usage metric."""
        SYSTEM_MEMORY_USAGE.set(bytes_used)
    
    @staticmethod
    def update_cpu_usage(percent: float):
        """Update CPU usage metric."""
        SYSTEM_CPU_USAGE.set(percent)
    
    @staticmethod
    def update_queue_size(size: int):
        """Update processing queue size."""
        PROCESSING_QUEUE_SIZE.set(size)


def setup_monitoring():
    """Setup monitoring configuration."""
    logger.info("Monitoring setup completed")


class HealthChecker:
    """Health check utilities."""
    
    def __init__(self):
        self.checks = {}
    
    def add_check(self, name: str, check_func):
        """Add a health check."""
        self.checks[name] = check_func
    
    async def run_checks(self) -> Dict[str, Any]:
        """Run all health checks."""
        results = {}
        
        for name, check_func in self.checks.items():
            try:
                result = await check_func()
                results[name] = {
                    "status": "healthy" if result else "unhealthy",
                    "details": result
                }
            except Exception as e:
                results[name] = {
                    "status": "error",
                    "details": str(e)
                }
        
        return results


# Global health checker instance
health_checker = HealthChecker() 