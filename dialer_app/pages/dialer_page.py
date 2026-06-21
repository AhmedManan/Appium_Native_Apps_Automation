"""
Dialer Page - Android Dialer App এর Keypad screen
Phone number dial করা, call করা সম্পর্কিত সব action এখানে
"""
import logging
from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class DialerPage(BasePage):
    """
    Dialer (Keypad) Screen এর Page Object।
    সব locator এবং action এই class এ encapsulate করা।
    """

    # ─── Locators ───────────────────────────────────────────────────

    # নম্বর দেখানোর field
    DIAL_INPUT          = (AppiumBy.ID, "com.android.dialer:id/digits")
    DIAL_INPUT_ALT      = (AppiumBy.ID, "com.android.contacts:id/digits")

    # Keypad Buttons (0–9, *, #)
    KEY_1   = (AppiumBy.ID, "com.android.dialer:id/one")
    KEY_2   = (AppiumBy.ID, "com.android.dialer:id/two")
    KEY_3   = (AppiumBy.ID, "com.android.dialer:id/three")
    KEY_4   = (AppiumBy.ID, "com.android.dialer:id/four")
    KEY_5   = (AppiumBy.ID, "com.android.dialer:id/five")
    KEY_6   = (AppiumBy.ID, "com.android.dialer:id/six")
    KEY_7   = (AppiumBy.ID, "com.android.dialer:id/seven")
    KEY_8   = (AppiumBy.ID, "com.android.dialer:id/eight")
    KEY_9   = (AppiumBy.ID, "com.android.dialer:id/nine")
    KEY_0   = (AppiumBy.ID, "com.android.dialer:id/zero")
    KEY_STAR    = (AppiumBy.ID, "com.android.dialer:id/star")
    KEY_HASH    = (AppiumBy.ID, "com.android.dialer:id/pound")

    # Call & Delete buttons
    CALL_BUTTON     = (AppiumBy.ID, "com.android.dialer:id/dialpad_floating_action_button")
    DELETE_BUTTON   = (AppiumBy.ID, "com.android.dialer:id/deleteButton")

    # Dial Pad open button (bottom navigation)
    DIALPAD_TAB     = (AppiumBy.ACCESSIBILITY_ID, "Dial pad")
    DIALPAD_TAB_ALT = (AppiumBy.XPATH,
                       '//android.widget.ImageButton[@content-desc="Dial pad"]')

    # FAB (Floating Action Button) - dial pad খোলার জন্য
    FAB_BUTTON      = (AppiumBy.ID, "com.android.dialer:id/fab")

    # ─── Key map (digit → locator) ──────────────────────────────────
    _KEY_MAP = {
        "0": (AppiumBy.ID, "com.android.dialer:id/zero"),
        "1": (AppiumBy.ID, "com.android.dialer:id/one"),
        "2": (AppiumBy.ID, "com.android.dialer:id/two"),
        "3": (AppiumBy.ID, "com.android.dialer:id/three"),
        "4": (AppiumBy.ID, "com.android.dialer:id/four"),
        "5": (AppiumBy.ID, "com.android.dialer:id/five"),
        "6": (AppiumBy.ID, "com.android.dialer:id/six"),
        "7": (AppiumBy.ID, "com.android.dialer:id/seven"),
        "8": (AppiumBy.ID, "com.android.dialer:id/eight"),
        "9": (AppiumBy.ID, "com.android.dialer:id/nine"),
        "*": (AppiumBy.ID, "com.android.dialer:id/star"),
        "#": (AppiumBy.ID, "com.android.dialer:id/pound"),
    }

    # ─── Actions ────────────────────────────────────────────────────

    def open_dial_pad(self) -> "DialerPage":
        """Dial Pad খোলে (যদি বন্ধ থাকে)"""
        if not self.is_element_visible(self.DIAL_INPUT):
            if self.is_element_visible(self.DIALPAD_TAB):
                self.click(self.DIALPAD_TAB)
            elif self.is_element_visible(self.FAB_BUTTON):
                self.click(self.FAB_BUTTON)
        logger.info("📞 Dial pad খোলা হয়েছে")
        return self

    def enter_phone_number(self, phone_number: str) -> "DialerPage":
        """
        Phone number এর প্রতিটি digit keypad এ press করে।
        Args:
            phone_number: ডায়াল করার নম্বর, যেমন '01712345678'
        """
        self.open_dial_pad()
        for digit in phone_number:
            if digit in self._KEY_MAP:
                self.click(self._KEY_MAP[digit])
            elif digit in ("+", "-", " "):
                continue  # separator skip করে
        logger.info(f"📱 নম্বর টাইপ করা হয়েছে: {phone_number}")
        return self

    def get_entered_number(self) -> str:
        """Dial input field এ বর্তমান নম্বর পড়ে"""
        return self.get_text(self.DIAL_INPUT)

    def tap_call_button(self) -> "DialerPage":
        """Call (green) button tap করে"""
        self.click(self.CALL_BUTTON)
        logger.info("📲 Call button tap করা হয়েছে")
        return self

    def tap_delete_button(self) -> "DialerPage":
        """Delete (backspace) button tap করে — এক character মুছে"""
        self.click(self.DELETE_BUTTON)
        return self

    def long_press_delete(self) -> "DialerPage":
        """Delete button long-press করে — সব মুছে ফেলে"""
        element = self.find_element(self.DELETE_BUTTON)
        from appium.webdriver.common.touch_action import TouchAction
        action = TouchAction(self.driver)
        action.long_press(element, duration=2000).release().perform()
        logger.info("🗑️ সব নম্বর মুছে ফেলা হয়েছে")
        return self

    def clear_dial_input(self) -> "DialerPage":
        """Dial input সম্পূর্ণ clear করে"""
        while self.is_element_present(self.DELETE_BUTTON):
            current = self.get_entered_number()
            if not current:
                break
            self.click(self.DELETE_BUTTON)
        return self

    def dial_number(self, phone_number: str) -> "DialerPage":
        """
        নম্বর enter করে call button tap করে — complete dial action।
        Args:
            phone_number: কল করার নম্বর
        """
        self.enter_phone_number(phone_number)
        self.tap_call_button()
        logger.info(f"☎️ Call করা হচ্ছে: {phone_number}")
        return self

    def is_dial_pad_visible(self) -> bool:
        """Dial pad দৃশ্যমান কিনা জানায়"""
        return self.is_element_visible(self.DIAL_INPUT)

    def is_call_button_visible(self) -> bool:
        """Call button দৃশ্যমান কিনা জানায়"""
        return self.is_element_visible(self.CALL_BUTTON)
