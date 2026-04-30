import pytest
from appium import webdriver
from typing import Any, Dict
from appium.options.common import AppiumOptions

capabilities: Dict[str, Any] = {
    "platformName": "Android",
    "deviceName": "emulator-5554",
    "automationName": "UiAutomator2",
    "appPackage": "org.videolan.vlc",
    # "appActivity": "org.videolan.vlc.StartActivity",
    "appium:adbExecTimeout": 60000,
    "appium:noReset": True,
    "appium:dontStopAppOnReset": True,
    "language": "en",
    "locale": "US",
    "appium:autoGrantPermissions": True
}

# FIX THE URL
url = "http://127.0.0.1:4723"   # correct for Appium 2.x

@pytest.fixture()
def driver():
    options = AppiumOptions().load_capabilities(capabilities)
    driver = webdriver.Remote(url, options=options)
    yield driver
    driver.quit()
