"""Test configuration for pytest-celery-utils."""

import pytest
import redis
from celery import Celery

print(f"Installed redis library version: {redis.__version__}")


@pytest.fixture
def celery_app():
    """Create a test Celery app with Redis broker."""
    app = Celery("test_app", broker="redis://localhost:6379/0")
    app.conf.update(
        task_always_eager=False,
        result_backend="redis://localhost:6379/0",
    )
    return app
