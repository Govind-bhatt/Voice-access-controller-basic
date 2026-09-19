from activation import verify_access_code
from browser_actions import run_local_demo
from code_red import trigger_code_red
from command_router import (
    command_requires_access,
    execute_command,
    find_command,
)
from config import ensure_project_folders
from database import initialize_database, log_command
from speech import OfflineSpeechRecognizer


CODE_RED_COMMANDS = {
    "code red",
    "activate code red",
    "emergency code red",
}


def normalize_text(text):
    """Normalize user text for simple matching."""
    return " ".join(text.lower().strip().split())


def is_code_red_command(text):
    """Return True when the explicit Code Red phrase was used."""
    return normalize_text(text) in CODE_RED_COMMANDS


def ask_confirmation(command_name):
    """Ask the user to approve an action before it runs."""
    answer = input(
        f"Confirm action '{command_name}'? Type yes or no: "
    ).strip().lower()

    return answer in {"yes", "y"}


def choose_activation_method():
    """
    Select one of the two prototype activation methods.

    Keyboard activation is represented by pressing Enter in this CLI
    workflow. The separate activation.py module tests Ctrl+Alt+V inside
    its application window.
    """
    print()
    print("Choose activation method:")
    print("1. Keyboard activation")
    print("2. Access-code activation")
    print("3. Exit")

    while True:
        choice = input("Enter 1, 2, or 3: ").strip()

        if choice == "1":
            print("Keyboard activation selected.")
            print("The CLI workflow is now activated.")
            return "keyboard"

        if choice == "2":
            print("Access-code activation selected.")
            if verify_access_code():
                return "access-code"

            print("Activation failed.")
            return None

        if choice == "3":
            return None

        print("Please enter 1, 2, or 3.")


def process_command(recognizer, activation_method):
    """Capture, route, authorize, confirm, execute, and log one command."""
    try:
        spoken_text = recognizer.recognize_once(duration_seconds=6)
    except (FileNotFoundError, RuntimeError) as error:
        print(f"Speech error: {error}")
        log_command(
            activation_method=activation_method,
            command_text="",
            access_granted=False,
            action_result=f"Speech error: {error}",
        )
        return True

    if not spoken_text:
        print("No speech was recognized.")
        log_command(
            activation_method=activation_method,
            command_text="",
            access_granted=False,
            action_result="No speech was recognized",
        )
        return True

    print(f"Recognized text: {spoken_text}")

    if is_code_red_command(spoken_text):
        print()
        print("Explicit Code Red command detected.")
        print("Configured action: request a Windows workstation lock.")
        print("No files will be deleted or destroyed.")

        if not verify_access_code():
            log_command(
                activation_method=activation_method,
                command_text=spoken_text,
                access_granted=False,
                action_result="Access denied; Code Red not executed",
                security_event="Code Red access denied",
            )
            return True

        confirmation = input(
            "Type LOCK to confirm the workstation lock, or anything else "
            "to cancel: "
        ).strip()

        if confirmation != "LOCK":
            result = "Code Red cancelled."
            print(result)
            log_command(
                activation_method=activation_method,
                command_text=spoken_text,
                access_granted=True,
                action_result=result,
                security_event="Code Red cancelled before lock",
            )
            return True

        print("The real workstation lock will now be requested.")
        result = trigger_code_red(perform_lock=True)
        print(result)
        return True

    command_name = find_command(spoken_text)

    if command_name is None:
        result = "Unsupported command."
        print(result)
        log_command(
            activation_method=activation_method,
            command_text=spoken_text,
            access_granted=False,
            action_result=result,
        )
        return True

    print(f"Matched command: {command_name}")

    requires_access = command_requires_access(command_name)

    if requires_access:
        if not verify_access_code():
            result = "Access denied."
            print(result)
            log_command(
                activation_method=activation_method,
                command_text=spoken_text,
                access_granted=False,
                action_result=result,
            )
            return True

    if command_name == "exit":
        result = "Exit requested."
        print(result)
        log_command(
            activation_method=activation_method,
            command_text=spoken_text,
            access_granted=True,
            action_result=result,
        )
        return False

    if not ask_confirmation(command_name):
        result = "Action cancelled."
        print(result)
        log_command(
            activation_method=activation_method,
            command_text=spoken_text,
            access_granted=True,
            action_result=result,
        )
        return True

    try:
        result = execute_command(command_name)
    except Exception as error:
        result = f"Action failed: {error}"

    print(result)

    log_command(
        activation_method=activation_method,
        command_text=spoken_text,
        access_granted=True,
        action_result=result,
    )

    return True


def main():
    ensure_project_folders()
    initialize_database()

    print("Voice-Controlled Desktop and Website Assistant")
    print("-----------------------------------------------")
    print("Voice recognition is offline.")
    print("Raw voice recordings are not saved.")
    print("Only allowlisted actions can run.")
    print()

    try:
        recognizer = OfflineSpeechRecognizer()
    except FileNotFoundError as error:
        print(f"Startup failed: {error}")
        return

    print("Vosk model loaded successfully.")

    while True:
        activation_method = choose_activation_method()

        if activation_method is None:
            print("Assistant closed.")
            return

        print()
        print("Assistant activated.")
        print("Speak one approved command.")
        print("Say 'exit' to close the assistant.")

        keep_running = process_command(
            recognizer=recognizer,
            activation_method=activation_method,
        )

        if not keep_running:
            print("Assistant closed.")
            return

        print()
        print("Returning to activation selection.")


if __name__ == "__main__":
    main()
