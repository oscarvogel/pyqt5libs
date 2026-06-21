import logging

import pytest

from pyqt5libs.core import logging as logging_helpers


def test_configure_logging_writes_to_file(tmp_path):
    log_file = tmp_path / "app.log"
    logger = logging_helpers.configure_logging(
        name="test_configure_logging_writes_to_file",
        level=logging.INFO,
        log_file=str(log_file),
        console=False,
    )

    logger.info("mensaje de prueba")
    for handler in logger.handlers:
        handler.flush()

    assert log_file.exists()
    assert "mensaje de prueba" in log_file.read_text(encoding="utf-8")


def test_configure_logging_does_not_duplicate_handlers(tmp_path):
    log_file = tmp_path / "app.log"
    logger_name = "test_configure_logging_does_not_duplicate_handlers"

    first = logging_helpers.configure_logging(name=logger_name, log_file=str(log_file), console=False)
    second = logging_helpers.configure_logging(name=logger_name, log_file=str(log_file), console=False)

    assert first is second
    file_handlers = [handler for handler in second.handlers if isinstance(handler, logging.FileHandler)]
    assert len(file_handlers) == 1


def test_capture_exceptions_can_suppress_exception(caplog):
    logger = logging.getLogger("test_capture_exceptions_can_suppress_exception")

    @logging_helpers.capture_exceptions(logger, message="falló", reraise=False)
    def fail():
        raise ValueError("boom")

    with caplog.at_level(logging.ERROR):
        assert fail() is None

    assert "falló" in caplog.text
    assert "boom" in caplog.text


def test_capture_exceptions_reraises_by_default():
    logger = logging.getLogger("test_capture_exceptions_reraises_by_default")

    @logging_helpers.capture_exceptions(logger)
    def fail():
        raise RuntimeError("boom")

    with pytest.raises(RuntimeError):
        fail()


def test_logging_module_all_is_defined():
    assert "configure_logging" in logging_helpers.__all__
    assert "capture_exceptions" in logging_helpers.__all__
