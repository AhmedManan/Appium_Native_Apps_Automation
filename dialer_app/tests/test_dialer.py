"""
test_dialer.py - Dialer (Keypad) ফিচার এর Test Cases
"""
import pytest
from pages.dialer_page import DialerPage


class TestDialer:
    """
    Dialer Keypad screen সম্পর্কিত সব test case।
    POM ব্যবহার করে প্রতিটি step page object method এ delegate করা।
    """

    # ─── TC-001 ─────────────────────────────────────────────────────

    def test_dial_pad_opens_successfully(self, driver):
        """
        TC-001: Dial pad সফলভাবে খোলে কিনা যাচাই করে।
        Steps:
            1. Dialer app চালু করে
            2. Dial pad খোলে
        Expected: Dial pad এর input field দৃশ্যমান হয়
        """
        page = DialerPage(driver)
        page.open_dial_pad()

        assert page.is_dial_pad_visible(), \
            "❌ Dial pad visible হওয়া উচিত ছিল"

    # ─── TC-002 ─────────────────────────────────────────────────────

    def test_enter_phone_number_on_keypad(self, driver):
        """
        TC-002: Keypad এ phone number সঠিকভাবে enter হয় কিনা।
        Steps:
            1. Dial pad খোলে
            2. নম্বর enter করে: 01712345678
        Expected: Dial input field এ নম্বরটি দেখায়
        """
        page = DialerPage(driver)
        number = "01712345678"
        page.open_dial_pad()
        page.enter_phone_number(number)

        entered = page.get_entered_number()
        assert entered == number, \
            f"❌ Expected '{number}', কিন্তু পাওয়া গেছে '{entered}'"

    # ─── TC-003 ─────────────────────────────────────────────────────

    def test_delete_button_removes_last_digit(self, driver):
        """
        TC-003: Delete button একটি করে digit মুছে।
        Steps:
            1. Dial pad খোলে
            2. '12345' enter করে
            3. Delete button tap করে
        Expected: '1234' দেখায় (শেষের '5' মুছে যায়)
        """
        page = DialerPage(driver)
        page.open_dial_pad()
        page.enter_phone_number("12345")
        page.tap_delete_button()

        entered = page.get_entered_number()
        assert entered == "1234", \
            f"❌ '1234' হওয়ার কথা, পাওয়া গেছে '{entered}'"

    # ─── TC-004 ─────────────────────────────────────────────────────

    def test_long_press_delete_clears_all(self, driver):
        """
        TC-004: Delete button long-press করলে সব digit মুছে যায়।
        Steps:
            1. Dial pad খোলে
            2. '9876' enter করে
            3. Delete button long-press করে
        Expected: Input field ফাঁকা হয়ে যায়
        """
        page = DialerPage(driver)
        page.open_dial_pad()
        page.enter_phone_number("9876")
        page.long_press_delete()

        entered = page.get_entered_number()
        assert entered == "", \
            f"❌ Input ফাঁকা হওয়ার কথা, পাওয়া গেছে '{entered}'"

    # ─── TC-005 ─────────────────────────────────────────────────────

    @pytest.mark.parametrize("number, description", [
        ("01711111111",  "Grameenphone নম্বর"),
        ("01811111111",  "Robi নম্বর"),
        ("01911111111",  "Banglalink নম্বর"),
        ("01611111111",  "Teletalk নম্বর"),
        ("*#06#",        "IMEI কোড"),
    ])
    def test_enter_various_phone_numbers(self, driver, number, description):
        """
        TC-005: বিভিন্ন ধরনের নম্বর সঠিকভাবে enter হয় কিনা।
        """
        page = DialerPage(driver)
        page.open_dial_pad()
        page.enter_phone_number(number)

        entered = page.get_entered_number()
        assert entered == number, \
            f"❌ [{description}] Expected '{number}', পাওয়া গেছে '{entered}'"

    # ─── TC-006 ─────────────────────────────────────────────────────

    def test_call_button_visible_after_number_entry(self, driver):
        """
        TC-006: নম্বর enter করার পর Call button দৃশ্যমান থাকে।
        Steps:
            1. Dial pad খোলে
            2. নম্বর enter করে
        Expected: Call button visible এবং clickable
        """
        page = DialerPage(driver)
        page.open_dial_pad()
        page.enter_phone_number("01700000000")

        assert page.is_call_button_visible(), \
            "❌ Call button visible হওয়ার কথা"

    # ─── TC-007 ─────────────────────────────────────────────────────

    def test_special_characters_on_dialpad(self, driver):
        """
        TC-007: Special character (* এবং #) keypad এ কাজ করে।
        Steps:
            1. Dial pad খোলে
            2. '*' এবং '#' enter করে
        Expected: Input field এ '*#' দেখায়
        """
        page = DialerPage(driver)
        page.open_dial_pad()
        page.enter_phone_number("*#")

        entered = page.get_entered_number()
        assert entered == "*#", \
            f"❌ '*#' হওয়ার কথা, পাওয়া গেছে '{entered}'"

    # ─── TC-008 ─────────────────────────────────────────────────────

    def test_empty_input_before_entry(self, driver):
        """
        TC-008: Dial pad খোলার পর input field শুরুতে ফাঁকা থাকে।
        """
        page = DialerPage(driver)
        page.open_dial_pad()

        entered = page.get_entered_number()
        assert entered == "", \
            f"❌ শুরুতে input ফাঁকা হওয়ার কথা, পাওয়া গেছে '{entered}'"
