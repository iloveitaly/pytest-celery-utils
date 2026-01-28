# Inspect Celery Queues with Pytest

I love Celery for background tasks, but testing them can be a headache. Usually, you have to run a worker or mock everything out. But sometimes you just want to know: "Did my task actually get queued in Redis?" and "Is the payload correct?"

That's why I put together `pytest-celery-utils`. It's a simple plugin that lets you peek directly into your Redis-backed Celery queues during your tests. No workers required—just pure inspection.

## Installation

Grab it with `uv`:

```bash
uv add --dev pytest-celery-utils
```

## Usage

Once installed, you get a `celery_utils` fixture. It's automatically available, so you can just drop it into your tests.

Here's how I use it to verify tasks are queuing up correctly:

```python
def test_task_queued(celery_utils):
    # Fire off a task
    my_task.delay(arg1, arg2)

    # Get all queued tasks
    tasks = celery_utils.get_all_queued_tasks()
    assert len(tasks) > 0

    # Get tasks of specific type
    my_tasks = celery_utils.jobs_of_type("myapp.tasks.my_task")
    assert len(my_tasks) == 1
```

You'll need a `celery_app` fixture configured in your `conftest.py` so the plugin knows where to look:

```python
import pytest
from celery import Celery

@pytest.fixture
def celery_app():
    # Make sure to point to your Redis instance
    return Celery("myapp", broker="redis://localhost:6379/0")
```

## Features

*   **Direct Redis Inspection:** Look at what's actually in your queue without needing a running worker.
*   **Task Counting:** Easily assert that `n` jobs of a specific type are queued.
*   **Job Filtering:** Grab all jobs or filter them by task name (string or callable).
*   **Queue Support:** Inspects all queues defined in your Celery app.
*   **Nested Data Access:** Includes a handy `dig` utility for traversing those deeply nested Celery message dicts.

## Limitations

Just a heads up: this is strictly for **Redis** brokers. If you're using RabbitMQ or SQS, this won't work for you. It's also designed for testing, so don't expect it to be blazing fast for production monitoring.

# [MIT License](LICENSE.md)
