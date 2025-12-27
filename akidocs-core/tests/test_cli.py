import os
import subprocess
from importlib.metadata import version
from pathlib import Path


def test_cli_produces_pdf(tmp_path):
    input_file = tmp_path / "test.md"
    output_file = tmp_path / "test.pdf"

    input_file.write_text("# Hello\n\nWorld")

    result = subprocess.run(
        [
            "uv",
            "run",
            "python",
            "-m",
            "akidocs_core",
            str(input_file),
            str(output_file),
        ],
        capture_output=True,
    )

    assert result.returncode == 0
    assert output_file.exists()
    assert output_file.stat().st_size > 0


def test_cli_version_long_flag():
    result = subprocess.run(
        ["uv", "run", "python", "-m", "akidocs_core", "--version"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert f"akidocs-core {version('akidocs-core')}" in result.stdout


def test_cli_version_short_flag():
    result = subprocess.run(
        ["uv", "run", "python", "-m", "akidocs_core", "-v"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert f"akidocs-core {version('akidocs-core')}" in result.stdout


def test_cli_help_long_flag():
    result = subprocess.run(
        ["uv", "run", "python", "-m", "akidocs_core", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert version("akidocs-core") in result.stdout
    assert "input" in result.stdout.lower()
    assert "output" in result.stdout.lower()


def test_cli_help_short_flag():
    result = subprocess.run(
        ["uv", "run", "python", "-m", "akidocs_core", "-h"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert version("akidocs-core") in result.stdout
    assert "input" in result.stdout.lower()
    assert "output" in result.stdout.lower()


def test_cli_open_long_flag(tmp_path):
    input_file = tmp_path / "test.md"
    output_file = tmp_path / "test.pdf"
    input_file.write_text("# Hello\n\nWorld")
    result = subprocess.run(
        [
            "uv",
            "run",
            "python",
            "-m",
            "akidocs_core",
            str(input_file),
            str(output_file),
            "--open",
        ],
        capture_output=True,
        text=True,
        env={**os.environ, "AKIDOCS_TEST_MODE": "1"},
    )
    assert result.returncode == 0
    assert output_file.exists()
    assert output_file.stat().st_size > 0
    assert "open" in result.stdout.lower()


def test_cli_open_short_flag(tmp_path):
    input_file = tmp_path / "test.md"
    output_file = tmp_path / "test.pdf"
    input_file.write_text("# Hello\n\nWorld")
    result = subprocess.run(
        [
            "uv",
            "run",
            "python",
            "-m",
            "akidocs_core",
            str(input_file),
            str(output_file),
            "-o",
        ],
        capture_output=True,
        text=True,
        env={**os.environ, "AKIDOCS_TEST_MODE": "1"},
    )
    assert result.returncode == 0
    assert output_file.exists()
    assert output_file.stat().st_size > 0
    assert "open" in result.stdout.lower()


def test_cli_style_long_flag(tmp_path):
    input_file = tmp_path / "test.md"
    output_file = tmp_path / "test.pdf"
    input_file.write_text("# Hello\n\nWorld")

    result = subprocess.run(
        [
            "uv",
            "run",
            "python",
            "-m",
            "akidocs_core",
            str(input_file),
            str(output_file),
            "--style",
            "generic",
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert output_file.exists()


def test_cli_style_short_flag(tmp_path):
    input_file = tmp_path / "test.md"
    output_file = tmp_path / "test.pdf"
    input_file.write_text("# Hello\n\nWorld")

    result = subprocess.run(
        [
            "uv",
            "run",
            "python",
            "-m",
            "akidocs_core",
            str(input_file),
            str(output_file),
            "-s",
            "generic",
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert output_file.exists()


def test_cli_style_long_flag_alias(tmp_path):
    input_file = tmp_path / "test.md"
    output_file = tmp_path / "test.pdf"
    input_file.write_text("# Hello\n\nWorld")

    result = subprocess.run(
        [
            "uv",
            "run",
            "python",
            "-m",
            "akidocs_core",
            str(input_file),
            str(output_file),
            "--style",
            "g",
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert output_file.exists()


def test_cli_style_short_flag_alias(tmp_path):
    input_file = tmp_path / "test.md"
    output_file = tmp_path / "test.pdf"
    input_file.write_text("# Hello\n\nWorld")

    result = subprocess.run(
        [
            "uv",
            "run",
            "python",
            "-m",
            "akidocs_core",
            str(input_file),
            str(output_file),
            "-s",
            "g",
        ],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert output_file.exists()
