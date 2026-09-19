import platform
import subprocess

from database import log_command


CODE_RED_TRIGGER = "code red"


def lock_workstation():
    """
    Lock the current workstation using the operating-system lock action.

    Windows is supported by this prototype. Linux and macOS return an
    explanatory message rather than attempting an unknown command.
    """
    operating_system = platform.system()

    if operating_system == "Windows":
        try:
            subprocess.Popen(
                ["rundll32.exe", "user32.dll,LockWorkStation"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NO_WINDOW,
            )
            return "Workstation lock requested."
        except OSError as error:
            return f"Workstation lock failed: {error}"

    if operating_system == "Linux":
        return (
            "Linux Code Red lock is not configured in this Windows-first "
            "prototype."
        )

    if operating_system == "Darwin":
        return (
            "macOS Code Red lock is not configured in this Windows-first "
            "prototype."
        )

    return f"Unsupported operating system: {operating_system}"


def trigger_code_red(perform_lock=False):
    """
    Trigger the configured Code Red response.

    perform_lock=False is used for safe module testing.
    perform_lock=True performs the actual workstation lock.
    """
    if not perform_lock:
        result = "Code Red test mode: no workstation lock was performed."

        log_command(
            activation_method="code-red-test",
            command_text=CODE_RED_TRIGGER,
            access_granted=True,
            action_result=result,
            security_event="Code Red test recorded; no lock performed",
        )

        return result

    result = lock_workstation()

    log_command(
        activation_method="code-red",
        command_text=CODE_RED_TRIGGER,
        access_granted=True,
        action_result=result,
        security_event="Code Red workstation-lock action requested",
    )

    return result


def main():
    print("Code Red module test")
    print("--------------------")
    print("Configured privacy action: lock the Windows workstation.")
    print("No files will be deleted.")
    print("No data will be destroyed.")
    print("No unknown applications will be closed.")
    print("No workstation lock will be performed in this test.")

    result = trigger_code_red(perform_lock=False)

    print(f"Result: {result}")
    print("--------------------")
    print("Code Red module test finished.")


if __name__ == "__main__":
    main()
