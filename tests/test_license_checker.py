from __future__ import annotations

from pathlib import Path

import pytest  # type: ignore

from .resources.utils import write_something_to_file
from license_checker import __license__
from license_checker.main import files_have_the_license
from license_checker.main import license_checker
from license_checker.main import license_in_file
from license_checker.main import main


def test_license_in_file(tmp_file_path: Path):
    write_something_to_file(
        tmp_file_path, f"license is in the file, LICENSE={__license__}",
    )
    assert license_in_file(tmp_file_path)


def test_license_not_in_file(tmp_file_path: Path):
    write_something_to_file(tmp_file_path, 'license not in the file')
    assert not license_in_file(tmp_file_path)


def test_cmd_license_not_in_file(tmp_file_path: Path, caplog):
    write_something_to_file(tmp_file_path, 'license not in the file')
    response = main(
        [
            '--files',
            str(tmp_file_path),
        ],
    )

    assert response == 0
    assert '✅' in caplog.text


def test_cmd_license_in_file(tmp_file_path: Path, caplog):
    write_something_to_file(
        tmp_file_path, f"license is in the file, {__license__}",
    )
    response = main(
        [
            '--files',
            str(tmp_file_path),
        ],
    )

    assert response == 0
    assert '✅' in caplog.text


def test_cmd_no_license_provided_as_parameter(tmp_file_path: Path):
    write_something_to_file(tmp_file_path, "I don't have any license")
    response = main(['--files', str(tmp_file_path)])
    assert response == 0


def test_cmd_no_files_provided(caplog):
    with pytest.raises(ValueError):
        main([])


def test_cmd_wrong_empty_files_flag(caplog):
    with pytest.raises(ValueError):
        main(['--files'])


def test_cmd_2_files_provided_one_does_not_contain_the_license(
    tmp_file_path: Path,
):
    write_something_to_file(tmp_file_path, f"I have the license={__license__}")
    another_file = tmp_file_path.parent / 'another_file.txt'
    write_something_to_file(another_file, 'I do not have the license')

    response = main(
        [
            '--files',
            str(tmp_file_path),
            str(another_file),
        ],
    )

    assert response == 1


def test_cmd_2_files_provided_both_contain_the_license(
    tmp_file_path: Path,
):
    write_something_to_file(
        tmp_file_path, f"I have the license: {__license__}",
    )
    another_file = tmp_file_path.parent / 'another_file.txt'
    write_something_to_file(another_file, f"I have it too: {__license__}")

    response = main(
        [
            '--files',
            str(tmp_file_path),
            str(another_file),
        ],
    )

    assert response == 0


def test_files_have_the_license_success(tmp_file_path: Path, caplog):
    write_something_to_file(tmp_file_path, f"I have the license={__license__}")

    result = files_have_the_license([tmp_file_path])

    assert result
    assert f"checking 1/1: {tmp_file_path}" in caplog.text


def test_files_have_the_license_failure(tmp_file_path: Path, caplog):
    write_something_to_file(tmp_file_path, f"I have the license={__license__}")
    another_file = tmp_file_path.parent / 'another_file.txt'
    write_something_to_file(another_file, "I don't")

    result = files_have_the_license([tmp_file_path, another_file])

    assert result
    assert f"checking 1/2: {tmp_file_path}" in caplog.text
    assert f"checking 2/2: {another_file}" in caplog.text


def test_license_checker_files_have_the_license(tmp_file_path: Path):
    write_something_to_file(tmp_file_path, f"I have the LICENSE={__license__}")
    another_file = tmp_file_path.parent / 'another_file.txt'
    write_something_to_file(
        another_file, f"I have it too license={__license__}",
    )

    result = license_checker(
        [tmp_file_path, another_file],
    )

    assert result == 1


def test_license_checker_not_files_have_the_license(tmp_file_path: Path):
    write_something_to_file(
        tmp_file_path, f"""I have the license, but not in the proper format: {
            __license__
        }""",
    )
    another_file = tmp_file_path.parent / 'another_file.txt'
    write_something_to_file(another_file, "I don't have it")

    result = license_checker(
        [tmp_file_path, another_file],
    )

    assert result == 0
