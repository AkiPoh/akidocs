import os
import subprocess
import sys


def open_file(path):
    """Open file in default application."""
    try:
        if sys.platform == "win32":
            os.startfile(path)
        elif sys.platform == "darwin":
            subprocess.run(["open", path], check=True)
        elif sys.platform.startswith("linux"):
            subprocess.run(["xdg-open", path], check=True)
        else:
            print(f"Cannot open file: unsupported platform '{sys.platform}'")
            return False
    except OSError as e:
        print(f"Cannot open file: {e}")
        return False
    except subprocess.CalledProcessError as e:
        print(f"Cannot open file: command failed with exit code {e.returncode}")
        return False
    return True
