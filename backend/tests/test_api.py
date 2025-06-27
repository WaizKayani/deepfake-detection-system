"""
API tests for the Media Authentication System.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock
import json

from main import app

client = TestClient(app)


class TestHealthEndpoints:
    """Test health check endpoints."""
    
    def test_health_check(self):
        """Test basic health check."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "media-authentication-system"
    
    def test_detailed_health_check(self):
        """Test detailed health check."""
        response = client.get("/api/v1/health/detailed")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "system" in data
        assert "components" in data
    
    def test_database_health_check(self):
        """Test database health check."""
        with patch('app.api.v1.endpoints.health.check_database_health', new_callable=AsyncMock) as mock_check:
            mock_check.return_value = True
            response = client.get("/api/v1/health/database")
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"
    
    def test_models_health_check(self):
        """Test models health check."""
        with patch('app.api.v1.endpoints.health.check_model_health', new_callable=AsyncMock) as mock_check:
            mock_check.return_value = True
            response = client.get("/api/v1/health/models")
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"


class TestUploadEndpoints:
    """Test file upload endpoints."""
    
    def test_upload_file_invalid_type(self):
        """Test upload with invalid file type."""
        files = {"file": ("test.txt", b"test content", "text/plain")}
        response = client.post("/api/v1/upload/", files=files)
        assert response.status_code == 400
        assert "Unsupported file type" in response.json()["detail"]
    
    def test_upload_file_valid_image(self):
        """Test upload with valid image file."""
        # Create a mock image file
        image_content = b"fake image content"
        files = {"file": ("test.jpg", image_content, "image/jpeg")}
        
        with patch('app.api.v1.endpoints.upload.save_uploaded_file', new_callable=AsyncMock) as mock_save:
            with patch('app.core.database.db_manager.save_file_upload', new_callable=AsyncMock) as mock_db:
                mock_save.return_value = True
                mock_db.return_value = True
                
                response = client.post("/api/v1/upload/", files=files)
                assert response.status_code == 200
                data = response.json()
                assert "file_id" in data
                assert data["file_type"] == "image"
                assert data["status"] == "uploaded"


class TestAnalyzeEndpoints:
    """Test analysis endpoints."""
    
    def test_get_analysis_result_not_found(self):
        """Test getting analysis result for non-existent file."""
        with patch('app.core.database.db_manager.get_analysis_result', new_callable=AsyncMock) as mock_get:
            mock_get.return_value = None
            response = client.get("/api/v1/analyze/nonexistent-id")
            assert response.status_code == 404
    
    def test_get_analysis_status_not_found(self):
        """Test getting analysis status for non-existent file."""
        with patch('app.core.database.db_manager.get_file_upload', new_callable=AsyncMock) as mock_get:
            mock_get.return_value = None
            response = client.get("/api/v1/analyze/nonexistent-id/status")
            assert response.status_code == 404
    
    def test_get_recent_analyses(self):
        """Test getting recent analyses."""
        with patch('app.core.database.db_manager.get_analysis_logs', new_callable=AsyncMock) as mock_get:
            mock_get.return_value = []
            response = client.get("/api/v1/analyze/recent/image")
            assert response.status_code == 200
            data = response.json()
            assert "file_type" in data
            assert "total_results" in data
    
    def test_get_analysis_statistics(self):
        """Test getting analysis statistics."""
        with patch('app.core.database.db_manager.get_statistics', new_callable=AsyncMock) as mock_get:
            mock_get.return_value = {
                "total_files": 0,
                "by_type": {"image": 0, "video": 0, "audio": 0},
                "by_prediction": {"real": 0, "fake": 0, "uncertain": 0},
                "average_confidence": 0.0
            }
            response = client.get("/api/v1/analyze/statistics/summary")
            assert response.status_code == 200
            data = response.json()
            assert "summary" in data


class TestLogsEndpoints:
    """Test logs endpoints."""
    
    def test_get_analysis_logs(self):
        """Test getting analysis logs."""
        with patch('app.core.database.db_manager.get_analysis_logs', new_callable=AsyncMock) as mock_get:
            mock_get.return_value = []
            response = client.get("/api/v1/logs/")
            assert response.status_code == 200
            data = response.json()
            assert "total_logs" in data
            assert "logs" in data
    
    def test_get_log_statistics(self):
        """Test getting log statistics."""
        with patch('app.core.database.db_manager.get_statistics', new_callable=AsyncMock) as mock_get:
            mock_get.return_value = {}
            response = client.get("/api/v1/logs/statistics")
            assert response.status_code == 200
            data = response.json()
            assert "statistics" in data
    
    def test_get_error_logs(self):
        """Test getting error logs."""
        with patch('app.core.database.db_manager.get_analysis_logs', new_callable=AsyncMock) as mock_get:
            mock_get.return_value = []
            response = client.get("/api/v1/logs/errors")
            assert response.status_code == 200
            data = response.json()
            assert "total_errors" in data
            assert "errors" in data


class TestModelsEndpoints:
    """Test model endpoints."""
    
    def test_get_model_status(self):
        """Test getting model status."""
        response = client.get("/api/v1/models/status")
        assert response.status_code == 200
        data = response.json()
        assert "models" in data
        assert "system" in data
    
    def test_get_model_info(self):
        """Test getting model information."""
        response = client.get("/api/v1/models/info/image")
        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert "type" in data
    
    def test_get_model_info_invalid(self):
        """Test getting model information for invalid model."""
        response = client.get("/api/v1/models/info/invalid")
        assert response.status_code == 404
    
    def test_get_model_performance(self):
        """Test getting model performance metrics."""
        response = client.get("/api/v1/models/performance")
        assert response.status_code == 200
        data = response.json()
        assert "image_model" in data
        assert "video_model" in data
        assert "audio_model" in data


class TestMetricsEndpoint:
    """Test Prometheus metrics endpoint."""
    
    def test_metrics_endpoint(self):
        """Test metrics endpoint returns Prometheus format."""
        response = client.get("/metrics")
        assert response.status_code == 200
        assert response.headers["content-type"] == "text/plain; version=0.0.4; charset=utf-8"
        content = response.text
        assert "# HELP" in content
        assert "# TYPE" in content


if __name__ == "__main__":
    pytest.main([__file__]) 