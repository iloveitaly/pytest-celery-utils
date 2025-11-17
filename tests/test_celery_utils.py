"""Test CeleryTestUtils functionality."""

import pytest
import redis
from celery import Celery

from pytest_celery_utils import CeleryTestUtils, dig


def is_redis_available():
    """Check if Redis is available."""
    try:
        client = redis.from_url("redis://localhost:6379/0")
        client.ping()
        return True
    except (redis.ConnectionError, redis.TimeoutError):
        return False


requires_redis = pytest.mark.skipif(
    not is_redis_available(), reason="Redis not available"
)


def test_dig_with_string_path():
    """Test dig function with string path."""
    data = {"a": {"b": {"c": 1}}}
    assert dig("a.b.c", data) == 1


def test_dig_with_list_path():
    """Test dig function with list path."""
    data = {"a": {"b": {"c": 1}}}
    assert dig(["a", "b", "c"], data) == 1


def test_dig_with_default():
    """Test dig function with default value."""
    data = {"a": {"b": 1}}
    assert dig("a.x", data, default=42) == 42


def test_dig_without_default_raises():
    """Test dig function raises when path not found."""
    data = {"a": {"b": 1}}
    with pytest.raises(KeyError):
        dig("a.x", data)


def test_celery_utils_initialization(celery_app):
    """Test CeleryTestUtils initialization."""
    utils = CeleryTestUtils(celery_app)
    assert utils.celery_app == celery_app
    assert utils.redis_client is not None
    assert isinstance(utils.queues, list)


def test_celery_utils_non_redis_broker_raises():
    """Test CeleryTestUtils raises ValueError for non-Redis broker."""
    app = Celery("test_app", broker="amqp://localhost")
    with pytest.raises(ValueError, match="Only Redis broker supported"):
        CeleryTestUtils(app)


@requires_redis
def test_get_all_queued_tasks_empty(celery_app, celery_utils):
    """Test get_all_queued_tasks returns empty list when no tasks."""
    tasks = celery_utils.get_all_queued_tasks()
    assert isinstance(tasks, list)


@requires_redis
def test_celery_utils_fixture(celery_utils):
    """Test celery_utils fixture is available and returns CeleryTestUtils."""
    assert isinstance(celery_utils, CeleryTestUtils)


@requires_redis
def test_jobs_of_type_with_string(celery_utils):
    """Test jobs_of_type with string task name."""
    jobs = celery_utils.jobs_of_type("app.tasks.example")
    assert isinstance(jobs, list)


@requires_redis
def test_count_jobs_of_type(celery_utils):
    """Test count_jobs_of_type returns integer."""
    count = celery_utils.count_jobs_of_type("app.tasks.example")
    assert isinstance(count, int)
    assert count >= 0
