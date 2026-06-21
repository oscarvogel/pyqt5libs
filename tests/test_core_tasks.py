import time

import pytest

from pyqt5libs.core.tasks import BackgroundTask, TaskResult, run_in_background


def test_background_task_success_result_and_callbacks():
    values = []
    done = []

    task = BackgroundTask(
        lambda a, b: a + b,
        2,
        3,
        on_success=values.append,
        on_done=done.append,
    ).start()

    result = task.join(timeout=1)

    assert isinstance(result, TaskResult)
    assert result.ok
    assert result.value == 5
    assert result.error is None
    assert values == [5]
    assert done == [result]


def test_background_task_error_result_and_callback():
    errors = []

    def fail():
        raise ValueError("boom")

    task = BackgroundTask(fail, on_error=errors.append).start()
    result = task.join(timeout=1)

    assert result is not None
    assert not result.ok
    assert isinstance(result.error, ValueError)
    assert errors == [result.error]


def test_run_in_background_starts_task():
    task = run_in_background(lambda: "ok")
    result = task.join(timeout=1)

    assert result.ok
    assert result.value == "ok"


def test_background_task_prevents_double_start_while_running():
    task = BackgroundTask(lambda: time.sleep(0.1)).start()

    with pytest.raises(RuntimeError):
        task.start()

    task.join(timeout=1)


def test_tasks_module_all_is_defined():
    from pyqt5libs.core import tasks

    assert "TaskResult" in tasks.__all__
    assert "BackgroundTask" in tasks.__all__
    assert "run_in_background" in tasks.__all__
