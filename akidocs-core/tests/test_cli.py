import os
import subprocess
from importlib.metadata import version

import pytest


def run_cli(*args, env=None, input=None):
    return subprocess.run(
        ["uv", "run", "python", "-m", "akidocs_core", *args],
        capture_output=True,
        text=True,
        env=env,
        input=input,
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


@pytest.fixture
def overwrite_files(tmp_path):
    input_file = tmp_path / "test.md"
    output_file = tmp_path / "test.pdf"
    input_file.write_text("# Hello")
    output_file.write_text("existing content")
    return input_file, output_file


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
    assert "opening" in result.stdout.lower()


def test_cli_open_short_flag(tmp_path):
    result = run_cli_with_files(
        tmp_path,
        "-o",
        env={**os.environ, "AKIDOCS_TEST_MODE": "1"},
    )
    assert "opening" in result.stdout.lower()


@pytest.mark.parametrize(
    "flag,style",
    [
        ("--style", "generic"),
        ("--style", "g"),
        ("-s", "generic"),
        ("-s", "g"),
        ("--style", "times"),
        ("--style", "t"),
        ("--style", "regard"),
        ("--style", "r"),
    ],
)
def test_cli_style(tmp_path, flag, style):
    run_cli_with_files(tmp_path, flag, style)


def test_overwrite_prompt_decline(overwrite_files):
    """Declining overwrite prompt should exit with error."""
    input_file, output_file = overwrite_files
    original_content = output_file.read_bytes()

    result = run_cli(str(input_file), str(output_file), input="n\n")

    assert result.returncode != 0
    assert output_file.read_bytes() == original_content


def test_overwrite_prompt_accept(overwrite_files):
    """Accepting overwrite prompt should proceed."""
    input_file, output_file = overwrite_files

    result = run_cli(str(input_file), str(output_file), input="y\n")

    assert result.returncode == 0
    assert "[y/n]" in result.stdout.lower()
    assert output_file.read_bytes() != b"existing content"


def test_non_interactive_errors_on_existing_file(overwrite_files):
    """--non-interactive should error instead of prompting."""
    input_file, output_file = overwrite_files
    original_content = output_file.read_bytes()

    result = run_cli(str(input_file), str(output_file), "--non-interactive")

    assert result.returncode != 0
    assert "exists" in result.stdout.lower() or "exists" in result.stderr.lower()
    assert output_file.read_bytes() == original_content


def test_non_interactive_short_flag(overwrite_files):
    """Short flag -n should work same as --non-interactive."""
    input_file, output_file = overwrite_files

    result = run_cli(str(input_file), str(output_file), "-n")

    assert result.returncode != 0
    assert "exists" in result.stdout.lower() or "exists" in result.stderr.lower()


def test_force_overwrites_without_prompt(overwrite_files):
    """--force should overwrite without prompting."""
    input_file, output_file = overwrite_files

    result = run_cli(str(input_file), str(output_file), "--force")

    assert result.returncode == 0
    assert "[y/n]" not in result.stdout.lower()
    assert output_file.read_bytes() != b"existing content"


def test_force_short_flag(overwrite_files):
    """Short flag -f should work same as --force."""
    input_file, output_file = overwrite_files

    result = run_cli(str(input_file), str(output_file), "-f")

    assert result.returncode == 0
    assert output_file.read_bytes() != b"existing content"


def test_force_overrides_non_interactive(overwrite_files):
    """--force should override --non-interactive and succeed."""
    input_file, output_file = overwrite_files

    result = run_cli(str(input_file), str(output_file), "-n", "-f")

    assert result.returncode == 0
    assert output_file.read_bytes() != b"existing content"


def test_cli_output_shows_style_info(tmp_path):
    """Output should show input, style info, and output."""
    input_file = tmp_path / "test.md"
    output_file = tmp_path / "test.pdf"
    input_file.write_text("# Hello")

    result = run_cli(str(input_file), str(output_file))

    assert "From test.md (Helvetica, generic) to test.pdf" in result.stdout
