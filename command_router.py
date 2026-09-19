import re

from browser_actions import run_local_demo
from desktop_actions import (
    open_browser,
    open_calculator,
    open_notepad,
    type_harmless_test_text,
)


PROTECTED_ACTIONS = {
    "open notepad",
    "open calculator",
    "open browser",
    "type harmless test text",
    "run browser demo",
}


def normalize_command(command_text):
    """Normalize punctuation, spacing, and capitalization."""
    text = command_text.lower().strip()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return " ".join(text.split())


def contains_any(text, words):
    """Return True if at least one complete word is present."""
    return any(re.search(rf"\b{re.escape(word)}\b", text) for word in words)


def find_command(command_text):
    """
    Convert natural-language phrases into safe canonical commands.

    This function only returns commands from the fixed allowlist.
    It never returns shell commands or arbitrary user text.
    """
    text = normalize_command(command_text)

    if not text:
        return None

    # Exit intent.
    if contains_any(
        text,
        {
            "exit",
            "quit",
            "close",
            "stop",
            "goodbye",
        },
    ) and contains_any(
        text,
        {
            "assistant",
            "program",
            "application",
            "yourself",
            "app",
            "voice",
            "quit",
            "exit",
        },
    ):
        return "exit"

    if text in {"exit", "quit", "close assistant", "close the assistant"}:
        return "exit"

    # Calculator intent.
    if contains_any(text, {"calculator", "calc"}) and contains_any(
        text,
        {
            "open",
            "launch",
            "start",
            "show",
            "display",
            "run",
            "bring",
            "please",
            "can",
            "could",
        },
    ):
        return "open calculator"

    # Notepad intent.
    if contains_any(text, {"notepad", "note", "notes"}) and contains_any(
        text,
        {
            "open",
            "launch",
            "start",
            "show",
            "display",
            "run",
            "bring",
            "please",
            "can",
            "could",
        },
    ):
        return "open notepad"

    # Browser intent.
    if contains_any(text, {"browser", "chrome", "web browser"}) and contains_any(
        text,
        {
            "open",
            "launch",
            "start",
            "show",
            "display",
            "run",
            "please",
            "can",
            "could",
        },
    ):
        return "open browser"

    # Local demo website intent.
    if (
        contains_any(text, {"demo", "website", "webpage", "web", "page"})
        and contains_any(
            text,
            {
                "open",
                "launch",
                "start",
                "show",
                "display",
                "run",
                "visit",
                "please",
                "can",
                "could",
            },
        )
    ):
        return "run browser demo"

    # Harmless typing intent.
    if contains_any(text, {"type", "write", "enter"}) and contains_any(
        text,
        {"test", "harmless", "demo"},
    ):
        return "type harmless test text"

    # Exact short commands remain supported.
    exact_commands = {
        "open calculator": "open calculator",
        "start calculator": "open calculator",
        "open notepad": "open notepad",
        "start notepad": "open notepad",
        "open browser": "open browser",
        "start browser": "open browser",
        "run demo": "run browser demo",
        "run browser demo": "run browser demo",
        "type test text": "type harmless test text",
        "type harmless test text": "type harmless test text",
    }

    return exact_commands.get(text)


def command_requires_access(command_name):
    """Return True when a command needs access-code verification."""
    return command_name in PROTECTED_ACTIONS


def execute_command(command_name):
    """Execute one already-approved canonical command."""
    if command_name == "open notepad":
        return open_notepad()

    if command_name == "open calculator":
        return open_calculator()

    if command_name == "open browser":
        return open_browser()

    if command_name == "type harmless test text":
        return type_harmless_test_text()

    if command_name == "run browser demo":
        return run_local_demo("voice assistant browser test")

    if command_name == "exit":
        return "Exit requested."

    return "Unsupported command."


def route_command(command_text):
    """Match text without executing an action."""
    command_name = find_command(command_text)

    if command_name is None:
        return {
            "recognized": False,
            "command": None,
            "requires_access": False,
            "message": "Unsupported command.",
        }

    return {
        "recognized": True,
        "command": command_name,
        "requires_access": command_requires_access(command_name),
        "message": f"Recognized command: {command_name}",
    }


def main():
    print("Natural-language command router test")
    print("-------------------------------------")

    test_commands = [
        "Please open the calculator",
        "Can you launch Notepad?",
        "Show me the demo website",
        "Could you start the web browser",
        "Please type harmless test text",
        "Close the assistant",
        "What are you?",
    ]

    for test_text in test_commands:
        result = route_command(test_text)
        print(f"Input: {test_text}")
        print(f"Result: {result}")
        print()

    print("-------------------------------------")
    print("Natural-language router test finished.")
    print("No desktop or browser action was executed.")


if __name__ == "__main__":
    main()
