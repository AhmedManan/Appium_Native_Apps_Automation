"""
Base Page - সমস্ত Page Object এর parent class
সব common method এখানে থাকবে যা সব page use করবে
"""
import logging
import time
from appium.webdriver.common.appiumby import AppiumBy
from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    ElementNotInteractableException
)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config.config import EXPLICIT_WAIT

logger = logging.getLogger(__name__)


class BasePage:
    """
    সব Page Object এর Base class।
    Common operations যেমন find, click, type এখানে defined।
    """

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, EXPLICIT_WAIT)

    # ─── Element Finders ────────────────────────────────────────────

    def find_element(self, locator: tuple):
        """Explicit wait দিয়ে element খোঁজে"""
        try:
            element = self.wait.until(
                EC.presence_of_element_located(locator)
            )
            return element
        except TimeoutException:
            logger.error(f"❌ Element পাওয়া যায়নি: {locator}")
            raise

    def find_elements(self, locator: tuple) -> list:
        """একাধিক element খোঁজে"""
        try:
            return self.wait.until(
                EC.presence_of_all_elements_located(locator)
            )
        except TimeoutException:
            logger.warning(f"⚠️ Elements পাওয়া যায়নি: {locator}")
            return []

    def find_clickable_element(self, locator: tuple):
        """Click করার জন্য ready element খোঁজে"""
        return self.wait.until(
            EC.element_to_be_clickable(locator)
        )

    # ─── Actions ────────────────────────────────────────────────────

    def click(self, locator: tuple) -> None:
        """Element এ click করে"""
        try:
            element = self.find_clickable_element(locator)
            element.click()
            logger.info(f"✅ Click করা হয়েছে: {locator}")
        except (TimeoutException, ElementNotInteractableException) as e:
            logger.error(f"❌ Click করতে সমস্যা {locator}: {e}")
            raise

    def send_keys(self, locator: tuple, text: str) -> None:
        """Element এ text input দেয়"""
        try:
            element = self.find_element(locator)
            element.clear()
            element.send_keys(text)
            logger.info(f"✅ Text লেখা হয়েছে '{text}' → {locator}")
        except Exception as e:
            logger.error(f"❌ Text লিখতে সমস্যা: {e}")
            raise

    def get_text(self, locator: tuple) -> str:
        """Element এর text পড়ে"""
        element = self.find_element(locator)
        text = element.text
        logger.info(f"📖 Text পড়া হয়েছে: '{text}'")
        return text

    def get_attribute(self, locator: tuple, attribute: str) -> str:
        """Element এর attribute পড়ে"""
        element = self.find_element(locator)
        return element.get_attribute(attribute)

    # ─── Visibility Checks ──────────────────────────────────────────

    def is_element_visible(self, locator: tuple, timeout: int = 5) -> bool:
        """Element visible আছে কিনা check করে"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    def is_element_present(self, locator: tuple, timeout: int = 5) -> bool:
        """Element DOM এ আছে কিনা check করে"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False

    # ─── Wait Helpers ───────────────────────────────────────────────

    def wait_for_element_visible(self, locator: tuple, timeout: int = EXPLICIT_WAIT):
        """Element visible হওয়া পর্যন্ত অপেক্ষা করে"""
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def wait_for_element_invisible(self, locator: tuple, timeout: int = EXPLICIT_WAIT):
        """Element invisible হওয়া পর্যন্ত অপেক্ষা করে"""
        return WebDriverWait(self.driver, timeout).until(
            EC.invisibility_of_element_located(locator)
        )

    def static_wait(self, seconds: float = 1.0) -> None:
        """Fixed time অপেক্ষা (শুধু প্রয়োজনে ব্যবহার করুন)"""
        time.sleep(seconds)

    # ─── App Controls ───────────────────────────────────────────────

    def press_back(self) -> None:
        """Android Back button press করে"""
        self.driver.press_keycode(4)
        logger.info("🔙 Back button press করা হয়েছে")

    def press_home(self) -> None:
        """Android Home button press করে"""
        self.driver.press_keycode(3)
        logger.info("🏠 Home button press করা হয়েছে")

    def swipe_up(self, duration: int = 800) -> None:
        """Screen এ উপরে swipe করে"""
        size = self.driver.get_window_size()
        start_x = size["width"] // 2
        start_y = int(size["height"] * 0.8)
        end_y   = int(size["height"] * 0.2)
        self.driver.swipe(start_x, start_y, start_x, end_y, duration)

    def swipe_down(self, duration: int = 800) -> None:
        """Screen এ নিচে swipe করে"""
        size = self.driver.get_window_size()
        start_x = size["width"] // 2
        start_y = int(size["height"] * 0.2)
        end_y   = int(size["height"] * 0.8)
        self.driver.swipe(start_x, start_y, start_x, end_y, duration)

    def take_screenshot(self, name: str) -> str:
        """Screenshot নেয় এবং path return করে"""
        path = f"reports/{name}_{int(time.time())}.png"
        self.driver.save_screenshot(path)
        logger.info(f"📸 Screenshot সংরক্ষিত: {path}")
        return path

    def scroll_to_text(self, text: str):
        """নির্দিষ্ট text এ scroll করে (UiScrollable)"""
        locator = (
            AppiumBy.ANDROID_UIAUTOMATOR,
            f'new UiScrollable(new UiSelector().scrollable(true))'
            f'.scrollIntoView(new UiSelector().text("{text}"))'
        )
        return self.find_element(locator)
