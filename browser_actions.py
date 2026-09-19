from pathlib import Path

from playwright.sync_api import Error as PlaywrightError
from playwright.sync_api import sync_playwright

from config import DEMO_PAGE_PATH


def demo_page_url():
    """Return the local demo page as a file URL."""
    page_path = Path(DEMO_PAGE_PATH).resolve()

    if not page_path.is_file():
        raise FileNotFoundError(
            f"Demo page was not found: {page_path}"
        )

    return page_path.as_uri()


def run_local_demo(test_text="voice assistant demo"):
    """
    Run the harmless local browser demonstration.

    The browser is opened visibly so the user can observe the action.
    """
    url = demo_page_url()

    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=False)
            page = browser.new_page()

            page.goto(url)
            page.locator("#test-text").fill(test_text)
            page.locator("#demo-button").click()

            result_text = page.locator("#result").inner_text()

            browser.close()

            return f"Browser demo completed: {result_text}"

    except PlaywrightError as error:
        return f"Browser automation failed: {error}"
    except Exception as error:
        return f"Browser demo failed: {error}"


def main():
    print("Safe browser actions module")
    print("---------------------------")
    print("Opening the local demo page...")

    result = run_local_demo("automated harmless test")

    print(result)
    print("---------------------------")
    print("Browser action test finished.")


if __name__ == "__main__":
    main()
