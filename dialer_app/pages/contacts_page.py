"""
Contacts Page - Contact তালিকা, অনুসন্ধান ও যোগ করার screen
"""
import logging
from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage

logger = logging.getLogger(__name__)


class ContactsPage(BasePage):
    """
    Contacts Screen এর Page Object।
    Contact খোঁজা, যোগ করা ও দেখার সব action এখানে।
    """

    # ─── Locators ───────────────────────────────────────────────────

    # Bottom navigation
    CONTACTS_TAB    = (AppiumBy.ACCESSIBILITY_ID, "Contacts")
    CONTACTS_TAB_ALT = (AppiumBy.XPATH,
                        '//android.widget.FrameLayout[@content-desc="Contacts"]')

    # Search
    SEARCH_ICON     = (AppiumBy.ID, "com.android.dialer:id/search_view_container")
    SEARCH_FIELD    = (AppiumBy.ID, "com.android.dialer:id/search_view")
    SEARCH_HINT     = (AppiumBy.XPATH, '//*[@text="Search contacts"]')
    SEARCH_CLEAR    = (AppiumBy.ID, "com.android.dialer:id/search_close_btn")

    # Contact list
    CONTACT_LIST    = (AppiumBy.ID, "com.android.dialer:id/recycler_view")
    CONTACT_ITEM    = (AppiumBy.XPATH,
                       '//android.widget.LinearLayout[contains(@resource-id,"contact")]')
    CONTACT_NAME    = (AppiumBy.ID, "com.android.dialer:id/cliv_name_textview")
    CONTACT_NUMBER  = (AppiumBy.ID, "com.android.dialer:id/cliv_data_text")

    # Add New Contact
    ADD_CONTACT_FAB = (AppiumBy.ID, "com.android.dialer:id/floating_action_button")
    ADD_CONTACT_ALT = (AppiumBy.ACCESSIBILITY_ID, "Add contact")

    # New Contact Form
    FIRST_NAME_FIELD = (AppiumBy.XPATH,
                        '//android.widget.EditText[@hint="First name"]')
    LAST_NAME_FIELD  = (AppiumBy.XPATH,
                        '//android.widget.EditText[@hint="Last name"]')
    PHONE_FIELD      = (AppiumBy.XPATH,
                        '//android.widget.EditText[@hint="Phone"]')
    SAVE_CONTACT_BTN = (AppiumBy.XPATH, '//*[@text="Save"]')

    # Contact detail page
    CONTACT_PHONE_NUMBER = (AppiumBy.ID, "com.android.dialer:id/header")
    CALL_CONTACT_BTN     = (AppiumBy.ID, "com.android.dialer:id/call_icon")

    # Empty state
    EMPTY_CONTACTS  = (AppiumBy.XPATH, '//*[contains(@text,"No contacts")]')

    # ─── Actions ────────────────────────────────────────────────────

    def go_to_contacts_tab(self) -> "ContactsPage":
        """Contacts tab এ navigate করে"""
        self.click(self.CONTACTS_TAB)
        logger.info("👥 Contacts tab এ গেছে")
        return self

    def is_contacts_list_visible(self) -> bool:
        """Contact list দৃশ্যমান কিনা"""
        return self.is_element_visible(self.CONTACT_LIST)

    def is_contacts_empty(self) -> bool:
        """Contact list ফাঁকা কিনা"""
        return self.is_element_visible(self.EMPTY_CONTACTS, timeout=3)

    def get_contact_count(self) -> int:
        """কতটি contact আছে জানায়"""
        contacts = self.find_elements(self.CONTACT_ITEM)
        count = len(contacts)
        logger.info(f"👤 Contact সংখ্যা: {count}")
        return count

    def search_contact(self, name: str) -> "ContactsPage":
        """
        Contact search করে।
        Args:
            name: যে নামে খুঁজবে
        """
        self.click(self.SEARCH_ICON)
        self.send_keys(self.SEARCH_FIELD, name)
        logger.info(f"🔍 Contact খুঁজছে: '{name}'")
        return self

    def clear_search(self) -> "ContactsPage":
        """Search field clear করে"""
        if self.is_element_visible(self.SEARCH_CLEAR, timeout=3):
            self.click(self.SEARCH_CLEAR)
        return self

    def get_search_results(self) -> list:
        """Search result এর contacts return করে"""
        return self.find_elements(self.CONTACT_ITEM)

    def tap_first_contact(self) -> "ContactsPage":
        """প্রথম contact এ tap করে"""
        contacts = self.find_elements(self.CONTACT_ITEM)
        if contacts:
            contacts[0].click()
            logger.info("👆 প্রথম contact এ tap করা হয়েছে")
        return self

    def tap_contact_by_name(self, name: str) -> "ContactsPage":
        """
        নাম দিয়ে contact খুঁজে tap করে।
        Args:
            name: Contact এর নাম
        """
        locator = (AppiumBy.XPATH, f'//*[@text="{name}"]')
        self.click(locator)
        logger.info(f"👆 '{name}' contact এ tap করা হয়েছে")
        return self

    def call_contact_from_detail(self) -> "ContactsPage":
        """Contact detail page থেকে call করে"""
        self.click(self.CALL_CONTACT_BTN)
        logger.info("📞 Contact কে call করা হচ্ছে")
        return self

    def add_new_contact(self, first_name: str, last_name: str,
                        phone: str) -> "ContactsPage":
        """
        নতুন contact যোগ করে।
        Args:
            first_name: প্রথম নাম
            last_name:  শেষ নাম
            phone:      ফোন নম্বর
        """
        self.click(self.ADD_CONTACT_FAB)
        self.send_keys(self.FIRST_NAME_FIELD, first_name)
        self.send_keys(self.LAST_NAME_FIELD, last_name)
        self.send_keys(self.PHONE_FIELD, phone)
        self.click(self.SAVE_CONTACT_BTN)
        logger.info(f"✅ Contact যোগ হয়েছে: {first_name} {last_name}, {phone}")
        return self

    def is_contact_found(self, name: str) -> bool:
        """Search result এ নির্দিষ্ট contact আছে কিনা"""
        locator = (AppiumBy.XPATH, f'//*[@text="{name}"]')
        return self.is_element_visible(locator, timeout=5)
