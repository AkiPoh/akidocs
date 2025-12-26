import subprocess
from pathlib import Path
from unittest.mock import patch

from akidocs_core.opener import open_file


def test_open_file_windows():
    with patch("akidocs_core.opener.sys.platform", "win32"):
        with patch("akidocs_core.opener.os.startfile", create=True) as mock_startfile:
            result = open_file(Path("test.pdf"))
            mock_startfile.assert_called_once_with(Path("test.pdf"))
            assert result is True


def test_open_file_macos():
    with patch("akidocs_core.opener.sys.platform", "darwin"):
        with patch("akidocs_core.opener.subprocess.run") as mock_run:
            result = open_file(Path("test.pdf"))
            mock_run.assert_called_once_with(["open", Path("test.pdf")], check=True)
            assert result is True


def test_open_file_linux():
    with patch("akidocs_core.opener.sys.platform", "linux"):
        with patch("akidocs_core.opener.subprocess.run") as mock_run:
            result = open_file(Path("test.pdf"))
            mock_run.assert_called_once_with(["xdg-open", Path("test.pdf")], check=True)
            assert result is True


def test_open_file_unsupported_platform(capsys):
    with patch("akidocs_core.opener.sys.platform", "freebsd"):
        result = open_file(Path("test.pdf"))
        assert result is False
        assert "unsupported platform" in capsys.readouterr().out


def test_open_file_oserror(capsys):
    with patch("akidocs_core.opener.sys.platform", "win32"):
        with patch(
            "akidocs_core.opener.os.startfile",
            side_effect=OSError("No application"),
            create=True,
        ):
            result = open_file(Path("test.pdf"))
            assert result is False
            assert "Cannot open file" in capsys.readouterr().out


def test_open_file_subprocess_error(capsys):
    with patch("akidocs_core.opener.sys.platform", "linux"):
        with patch(
            "akidocs_core.opener.subprocess.run",
            side_effect=subprocess.CalledProcessError(1, "xdg-open"),
        ):
            result = open_file(Path("test.pdf"))
            assert result is False
            assert "Cannot open file" in capsys.readouterr().out
