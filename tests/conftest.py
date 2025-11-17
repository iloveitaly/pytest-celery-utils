"""Test configuration for pytest-celery-utils."""

import pytest
from celery import Celery


@pytest.fixture
def celery_app():
    """Create a test Celery app with Redis broker."""
    app = Celery("test_app", broker="redis://localhost:6379/0")
    app.conf.update(
        task_always_eager=False,
        result_backend="redis://localhost:6379/0",
    )
    return app
