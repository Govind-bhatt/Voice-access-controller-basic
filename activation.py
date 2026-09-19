import getpass
import hmac
import tkinter as tk

from config import ACCESS_CODE, MAX_ACCESS_ATTEMPTS


def verify_access_code():
    """
    Request and verify the configured access code.

    The entered code is not displayed, printed, or saved to SQLite.
    """
    if not ACCESS_CODE:
        print("Access code is not configured.")
        return False

    for _ in range(MAX_ACCESS_ATTEMPTS):
        entered_code = getpass.getpass("Enter access code: ")

        if hmac.compare_digest(entered_code, ACCESS_CODE):
            print("Access granted.")
            return True

        print("Access denied.")

    print("Access denied. Maximum attempts reached for this session.")
    return False


class ActivationWindow:
    """Test in-application Ctrl+Alt+V keyboard activation."""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Voice Assistant Activation Test")
        self.root.geometry("500x220")
        self.root.resizable(False, False)

        self.status_label = tk.Label(
            self.root,
            text="Press Ctrl+Alt+V to request activation.",
            font=("Arial", 14),
            wraplength=440,
        )
        self.status_label.pack(pady=35)

        close_button = tk.Button(
            self.root,
            text="Close",
            command=self.root.destroy,
            width=15,
        )
        close_button.pack()

        self.root.bind("<Control-Alt-v>", self.handle_keyboard_activation)
        self.root.bind("<Control-Alt-V>", self.handle_keyboard_activation)

    def handle_keyboard_activation(self, _event=None):
        self.status_label.config(text="Keyboard activation detected.")

        self.root.withdraw()

        try:
            activated = verify_access_code()
        finally:
            self.root.deiconify()

        if activated:
            self.status_label.config(text="Access granted.")
        else:
            self.status_label.config(text="Access denied.")

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    print("Keyboard activation test")
    print("The assistant window must be focused.")
    print("Press Ctrl+Alt+V inside the window.")

    ActivationWindow().run()
