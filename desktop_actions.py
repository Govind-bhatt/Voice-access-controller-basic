import platform
import shutil
import subprocess
import time

import pyautogui


SAFE_TEST_TEXT = "This is harmless voice-assistant test text."


def _run_windows_command(command):
    """Run a Windows command without opening an extra console window."""
    return subprocess.Popen(
        command,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=subprocess.CREATE_NO_WINDOW,
    )


def open_notepad():
    """Open the Windows Notepad application."""
    if platform.system() != "Windows":
        return "Notepad action is currently implemented for Windows only."

    _run_windows_command(["notepad.exe"])
    return "Notepad opened."


def open_calculator():
    """Open the Windows Calculator application."""
    if platform.system() != "Windows":
        return "Calculator action is currently implemented for Windows only."

    _run_windows_command(["calc.exe"])
    return "Calculator opened."


def open_browser():
    """Open the system's default browser."""
    if platform.system() == "Windows":
        _run_windows_command(["cmd", "/c", "start", "", "https://example.com"] )
        return "Default browser opened."

    browser = shutil.which("xdg-open")
    if browser:
        subprocess.Popen(
            [browser, "https://example.com"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
         )
        return "Default browser opened."

    return "No supported default-browser command was found."


def type_harmless_test_text():
    """
    Type harmless text into the currently focused window.

    The user must focus a clearly identified test window before calling this
    function. No passwords or personal information should be entered.
    """
    pyautogui.write(SAFE_TEST_TEXT, interval=0.02)
    return "Harmless test text typed into the focused window."


def list_safe_actions():
    """Return the desktop actions currently allowed by the prototype."""
    return [
        "open notepad",
        "open calculator",
        "open browser",
        "type harmless test text",
    ]


def main():
    print("Safe desktop actions module")
    print("---------------------------")
    print("No desktop application will be opened by this listing test.")
    print("Allowed actions:")

    for action in list_safe_actions():
        print(f"- {action}")

    print("---------------------------")
    print("Desktop action module loaded successfully.")


if __name__ == "__main__":
    main()
