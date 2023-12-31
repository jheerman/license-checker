from __future__ import annotations

import logging
from pathlib import Path

import pytest  # type: ignore
from _pytest.logging import caplog as _caplog  # type: ignore # noqa F401
from loguru import logger  # type: ignore


@pytest.fixture
def tmp_file_path(tmp_path: Path) -> Path:
    file_path = tmp_path / 'file.txt'
    return file_path


@pytest.fixture
def caplog(_caplog):  # noqa F811
    class PropagateHandler(logging.Handler):
        def emit(self, record):
            logging.getLogger(record.name).handle(record)

    handler_id = logger.add(PropagateHandler(), format='{message} {extra}')
    yield _caplog
    logger.remove(handler_id)
