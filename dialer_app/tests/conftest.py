"""
conftest.py - Pytest Fixtures
Driver setup/teardown এবং shared fixtures এখানে
"""
import os
import logging
import pytest
from utils.driver_factory import DriverFactory
from pages.dialer_page   import DialerPage
from pages.call_log_page import CallLogPage
from pages.contacts_page import ContactsPage

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s — %(message)s",
    datefmt="%H:%M:%S",
)


# ─── Driver Fixture ─────────────────────────────────────────────────────────

@pytest.fixture(scope="function")
def driver():
    """
    প্রতিটি test function এর জন্য নতুন Appium driver তৈরি করে।
    Test শেষে driver quit করে।
    """
    _driver = DriverFactory.create_driver()
    yield _driver
    DriverFactory.quit_driver(_driver)


# ─── Page Fixtures ───────────────────────────────────────────────────────────

@pytest.fixture(scope="function")
def dialer_page(driver):
    """DialerPage instance return করে"""
    return DialerPage(driver)


@pytest.fixture(scope="function")
def call_log_page(driver):
    """CallLogPage instance return করে"""
    return CallLogPage(driver)


@pytest.fixture(scope="function")
def contacts_page(driver):
    """ContactsPage instance return করে"""
    return ContactsPage(driver)


# ─── Screenshot on Failure ───────────────────────────────────────────────────

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Test fail হলে automatically screenshot নেয়।
    """
    outcome = yield
    report  = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")
        if driver:
            os.makedirs("reports", exist_ok=True)
            screenshot_path = f"reports/FAIL_{item.name}.png"
            driver.save_screenshot(screenshot_path)
            logging.getLogger(__name__).error(
                f"📸 Failure screenshot: {screenshot_path}"
            )
