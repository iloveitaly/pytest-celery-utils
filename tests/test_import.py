"""Test pytest-celery-utils."""

import pytest_celery_utils


def test_import() -> None:
    """Test that the  can be imported."""
    assert isinstance(pytest_celery_utils.__name__, str)


def test_version() -> None:
    """Test that the version is available."""
    assert isinstance(pytest_celery_utils.__version__, str)
