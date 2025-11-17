# pytest-celery-utils

Pytest plugin for inspecting Celery task queues in Redis during tests.

This plugin provides utilities for testing Celery tasks without running workers, allowing you to inspect queued tasks directly from Redis.

## Installation

```bash
uv add pytest-celery-utils
```

## Requirements

- Python 3.11+
- Celery with Redis broker
- Redis server

## Usage

The plugin automatically provides a `celery_utils` fixture that you can use in your tests:

```python
def test_task_queued(celery_utils):
    # Queue a task
    my_task.delay(arg1, arg2)

    # Check if task is queued
    assert celery_utils.count_jobs_of_type("myapp.tasks.my_task") == 1

    # Get all queued tasks
    tasks = celery_utils.get_all_queued_tasks()
    assert len(tasks) > 0

    # Get tasks of specific type
    my_tasks = celery_utils.jobs_of_type("myapp.tasks.my_task")
    assert len(my_tasks) == 1
```

### Configuration

You need to provide a `celery_app` fixture in your test configuration:

```python
# conftest.py
import pytest
from celery import Celery

@pytest.fixture
def celery_app():
    app = Celery("myapp", broker="redis://localhost:6379/0")
    return app
```

## API Reference

### CeleryTestUtils

The main utility class providing methods for inspecting Celery queues.

#### Methods

- **`get_all_queued_tasks() -> list[dict[str, Any]]`**
  Returns all tasks currently in the Redis queue(s).

- **`jobs_of_type(task: Union[str, Callable]) -> list[dict[str, Any]]`**
  Returns all tasks of a specific type. Can accept either a task name string or a task function.

- **`count_jobs_of_type(task: Union[str, Callable]) -> int`**
  Returns the count of tasks of a specific type.

### Utility Functions

- **`dig(path, data, *, default=None)`**
  Navigate nested dictionaries using dot-path notation or list of keys.

  ```python
  from pytest_celery_utils import dig

  data = {"headers": {"task": "myapp.tasks.example"}}
  task_name = dig("headers.task", data)
  # or
  task_name = dig(["headers", "task"], data)
  ```

## Limitations

- Only supports Redis broker (not RabbitMQ or other brokers)
- Designed for testing without workers running
- Not optimized for performance (intended for testing only)

## License

MIT

## Author

Michael Bianco (mike@mikebian.co)
