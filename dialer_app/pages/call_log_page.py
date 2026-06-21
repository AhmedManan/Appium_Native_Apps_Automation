"""
Call Log Page - সাম্প্রতিক, মিসড ও সব কলের তালিকা
"""
import logging
from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class CallLogPage(BasePage):
    """
    Call Log (Recent Calls) Screen এর Page Object।
    কলের ইতিহাস দেখা ও manage করার সব action এখানে।
    """

    # ─── Locators ───────────────────────────────────────────────────

    # Bottom navigation - Recents tab
    RECENTS_TAB     = (AppiumBy.ACCESSIBILITY_ID, "Recents")
    RECENTS_TAB_ALT = (AppiumBy.XPATH,
                       '//android.widget.FrameLayout[@content-desc="Recents"]')

    # Call log list এবং items
    CALL_LOG_LIST   = (AppiumBy.ID, "com.android.dialer:id/recycler_view")
    CALL_LOG_ITEM   = (AppiumBy.XPATH,
                       '//android.widget.FrameLayout[contains(@resource-id,"call_log")]')

    # Call log item fields
    CALL_NAME       = (AppiumBy.ID, "com.android.dialer:id/contact_name")
    CALL_NUMBER     = (AppiumBy.ID, "com.android.dialer:id/number")
    CALL_TYPE       = (AppiumBy.ID, "com.android.dialer:id/call_type")
    CALL_TIME       = (AppiumBy.ID, "com.android.dialer:id/call_time")

    # Filter tabs (All / Missed)
    TAB_ALL         = (AppiumBy.XPATH, '//*[@text="ALL"]')
    TAB_MISSED      = (AppiumBy.XPATH, '//*[@text="MISSED"]')

    # Empty state
    EMPTY_CALL_LOG  = (AppiumBy.ID, "com.android.dialer:id/empty_list_view")
    EMPTY_TEXT      = (AppiumBy.XPATH,
                       '//*[contains(@text,"No recent calls")]')

    # Call log item options
    CALL_BACK_BUTTON = (AppiumBy.ID, "com.android.dialer:id/primary_action_button")

    # Clear / Delete menu
    OVERFLOW_MENU   = (AppiumBy.XPATH,
                       '//android.widget.ImageView[@content-desc="More options"]')
    CLEAR_ALL_OPTION = (AppiumBy.XPATH, '//*[@text="Clear call history"]')
    DELETE_OPTION   = (AppiumBy.XPATH, '//*[@text="Delete"]')
    OK_BUTTON       = (AppiumBy.XPATH, '//*[@text="OK"]')
    CONFIRM_CLEAR   = (AppiumBy.XPATH, '//*[@text="Clear"]')

    # ─── Actions ────────────────────────────────────────────────────

    def go_to_recents_tab(self) -> "CallLogPage":
        """Recents / Call Log tab এ navigate করে"""
        self.click(self.RECENTS_TAB)
        logger.info("📋 Recents (Call Log) tab এ গেছে")
        return self

    def is_call_log_visible(self) -> bool:
        """Call log list দৃশ্যমান কিনা"""
        return self.is_element_visible(self.CALL_LOG_LIST)

    def is_call_log_empty(self) -> bool:
        """Call log খালি কিনা জানায়"""
        return (self.is_element_visible(self.EMPTY_CALL_LOG, timeout=3)
                or self.is_element_visible(self.EMPTY_TEXT, timeout=3))

    def get_call_log_entries(self) -> list:
        """Call log এর সব entry elements return করে"""
        if self.is_call_log_empty():
            logger.info("📭 Call log ফাঁকা")
            return []
        return self.find_elements(self.CALL_LOG_ITEM)

    def get_call_log_count(self) -> int:
        """কতটি call log entry আছে তা return করে"""
        entries = self.get_call_log_entries()
        count = len(entries)
        logger.info(f"📊 Call log entry সংখ্যা: {count}")
        return count

    def get_first_call_name(self) -> str:
        """প্রথম call log entry এর name পড়ে"""
        return self.get_text(self.CALL_NAME)

    def tap_first_call_entry(self) -> "CallLogPage":
        """প্রথম call log entry তে tap করে"""
        entries = self.get_call_log_entries()
        if entries:
            entries[0].click()
            logger.info("☎️ প্রথম call entry তে tap করা হয়েছে")
        return self

    def tap_call_back(self) -> "CallLogPage":
        """Call back button (সবুজ phone icon) tap করে"""
        self.click(self.CALL_BACK_BUTTON)
        logger.info("🔄 Call back করা হচ্ছে")
        return self

    def filter_by_missed_calls(self) -> "CallLogPage":
        """Missed calls ফিল্টার করে"""
        self.click(self.TAB_MISSED)
        logger.info("🔴 Missed calls ফিল্টার করা হয়েছে")
        return self

    def filter_all_calls(self) -> "CallLogPage":
        """সব call দেখায়"""
        self.click(self.TAB_ALL)
        logger.info("📋 All calls দেখানো হচ্ছে")
        return self

    def clear_call_history(self) -> "CallLogPage":
        """সম্পূর্ণ call history মুছে ফেলে"""
        self.click(self.OVERFLOW_MENU)
        self.click(self.CLEAR_ALL_OPTION)
        # Confirmation dialog
        if self.is_element_visible(self.OK_BUTTON, timeout=3):
            self.click(self.OK_BUTTON)
        elif self.is_element_visible(self.CONFIRM_CLEAR, timeout=3):
            self.click(self.CONFIRM_CLEAR)
        logger.info("🗑️ Call history মুছে ফেলা হয়েছে")
        return self
