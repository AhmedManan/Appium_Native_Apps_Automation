"""
Driver Factory - Appium WebDriver instance তৈরি ও manage করে
"""
import logging
from appium import webdriver
from appium.options.android import UiAutomator2Options
from config.config import APPIUM_SERVER_URL, ANDROID_CAPABILITIES, IMPLICIT_WAIT

logger = logging.getLogger(__name__)


class DriverFactory:
    """Appium Driver তৈরি ও ধ্বংস করার জন্য Factory class"""

    @staticmethod
    def create_driver() -> webdriver.Remote:
        """
        UiAutomator2 options দিয়ে Appium driver তৈরি করে।
        Returns:
            webdriver.Remote: Appium driver instance
        """
        try:
            options = UiAutomator2Options()
            for key, value in ANDROID_CAPABILITIES.items():
                setattr(options, key, value)

            driver = webdriver.Remote(
                command_executor=APPIUM_SERVER_URL,
                options=options
            )
            driver.implicitly_wait(IMPLICIT_WAIT)
            logger.info("✅ Appium driver সফলভাবে তৈরি হয়েছে")
            return driver

        except Exception as e:
            logger.error(f"❌ Driver তৈরিতে সমস্যা: {e}")
            raise

    @staticmethod
    def quit_driver(driver: webdriver.Remote) -> None:
        """
        Driver session শেষ করে।
        Args:
            driver: Appium driver instance
        """
        if driver:
            try:
                driver.quit()
                logger.info("✅ Driver session সফলভাবে বন্ধ হয়েছে")
            except Exception as e:
                logger.warning(f"⚠️ Driver বন্ধ করতে সমস্যা: {e}")
