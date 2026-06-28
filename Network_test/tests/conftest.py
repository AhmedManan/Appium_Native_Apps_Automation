import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options


@pytest.fixture(scope="function")
def driver():
    # Setup Android device capabilities
    options = UiAutomator2Options()
    options.platform_name = "Android"
    options.automation_name = "UiAutomator2"
    options.device_name = "acb2cc1e"  # Device name or adb ID
    options.no_reset = True  # Prevents resetting app data between sessions


    # Appium server URL
    driver = webdriver.Remote("http://127.0.0.1:4723", options=options)

    yield driver

    driver.quit()