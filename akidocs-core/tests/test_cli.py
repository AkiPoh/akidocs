import os
import subprocess
from importlib.metadata import version
from pathlib import Path

import pytest


def run_cli(*args, env=None):
    return subprocess.run(
        ["uv", "run", "python", "-m", "akidocs_core", *args],
        capture_output=True,
        text=True,
        env=env,
    )


def run_cli_with_files(tmp_path, *extra_args, env=None):
    input_file = tmp_path / "test.md"
    output_file = tmp_path / "test.pdf"
    input_file.write_text("# Hello\n\nWorld")

    result = run_cli(str(input_file), str(output_file), *extra_args, env=env)

    assert result.returncode == 0
    assert output_file.exists()
    assert output_file.stat().st_size > 0

    return result


def test_cli_produces_pdf(tmp_path):
    run_cli_with_files(tmp_path)


def test_cli_version_long_flag():
    result = run_cli("--version")
    assert result.returncode == 0
    assert f"akidocs-core {version('akidocs-core')}" in result.stdout


def test_cli_version_short_flag():
    result = run_cli("-v")
    assert result.returncode == 0
    assert f"akidocs-core {version('akidocs-core')}" in result.stdout


def test_cli_help_long_flag():
    result = run_cli("--help")
    assert result.returncode == 0
    assert version("akidocs-core") in result.stdout
    assert "input" in result.stdout.lower()
    assert "output" in result.stdout.lower()


def test_cli_help_short_flag():
    result = run_cli("-h")
    assert result.returncode == 0
    assert version("akidocs-core") in result.stdout
    assert "input" in result.stdout.lower()
    assert "output" in result.stdout.lower()


def test_cli_open_long_flag(tmp_path):
    result = run_cli_with_files(
        tmp_path,
        "--open",
        env={**os.environ, "AKIDOCS_TEST_MODE": "1"},
    )
    assert "open" in result.stdout.lower()


def test_cli_open_short_flag(tmp_path):
    result = run_cli_with_files(
        tmp_path,
        "-o",
        env={**os.environ, "AKIDOCS_TEST_MODE": "1"},
    )
    assert "open" in result.stdout.lower()


@pytest.mark.parametrize(
    "flag,style",
    [
        ("--style", "generic"),
        ("--style", "g"),
        ("-s", "generic"),
        ("-s", "g"),
        ("--style", "modern"),
        ("--style", "m"),
        ("--style", "regard"),
        ("--style", "r"),
    ],
)
def test_cli_style(tmp_path, flag, style):
    run_cli_with_files(tmp_path, flag, style)
