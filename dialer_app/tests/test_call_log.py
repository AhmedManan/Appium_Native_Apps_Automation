"""
test_call_log.py - Call Log (Recent Calls) ফিচার এর Test Cases
"""
import pytest
from pages.call_log_page import CallLogPage


class TestCallLog:
    """
    Call Log screen সম্পর্কিত সব test case।
    """

    # ─── TC-101 ─────────────────────────────────────────────────────

    def test_navigate_to_recents_tab(self, driver):
        """
        TC-101: Recents tab এ সফলভাবে navigate করা যায়।
        Steps:
            1. Dialer app চালু
            2. Recents tab এ click
        Expected: Call log list বা empty state দেখায়
        """
        page = CallLogPage(driver)
        page.go_to_recents_tab()

        visible = (page.is_call_log_visible()
                   or page.is_call_log_empty())
        assert visible, "❌ Recents tab এর content দেখা যাচ্ছে না"

    # ─── TC-102 ─────────────────────────────────────────────────────

    def test_call_log_shows_entries_or_empty(self, driver):
        """
        TC-102: Call log হয় entries দেখায়, অথবা empty state দেখায়।
        """
        page = CallLogPage(driver)
        page.go_to_recents_tab()

        # যেকোনো একটি অবস্থা থাকতে পারে
        has_entries = page.get_call_log_count() > 0
        is_empty    = page.is_call_log_empty()
        assert has_entries or is_empty, \
            "❌ Call log এর কোনো state নির্ধারণ করা গেলো না"

    # ─── TC-103 ─────────────────────────────────────────────────────

    @pytest.mark.skipif_empty_log
    def test_call_log_count_is_positive(self, driver):
        """
        TC-103: Call history থাকলে count 0 এর বেশি।
        (Call history ফাঁকা থাকলে skip করুন)
        """
        page = CallLogPage(driver)
        page.go_to_recents_tab()

        if page.is_call_log_empty():
            pytest.skip("Call history ফাঁকা — test প্রযোজ্য নয়")

        count = page.get_call_log_count()
        assert count > 0, "❌ Call log এ কমপক্ষে ১টি entry থাকার কথা"

    # ─── TC-104 ─────────────────────────────────────────────────────

    def test_filter_missed_calls_tab(self, driver):
        """
        TC-104: 'MISSED' filter tab সফলভাবে কাজ করে।
        Steps:
            1. Recents tab এ যায়
            2. MISSED tab এ click করে
        Expected: Missed calls filter হয় (empty বা entries দেখায়)
        """
        page = CallLogPage(driver)
        page.go_to_recents_tab()
        page.filter_by_missed_calls()

        visible = (page.is_call_log_visible()
                   or page.is_call_log_empty())
        assert visible, "❌ Missed calls filter কাজ করেনি"

    # ─── TC-105 ─────────────────────────────────────────────────────

    def test_switch_between_all_and_missed_tabs(self, driver):
        """
        TC-105: ALL এবং MISSED tab এর মধ্যে switch করা যায়।
        Steps:
            1. Recents tab এ যায়
            2. MISSED tab এ যায়
            3. ALL tab এ ফিরে আসে
        Expected: উভয় tab সঠিকভাবে কাজ করে
        """
        page = CallLogPage(driver)
        page.go_to_recents_tab()
        page.filter_by_missed_calls()
        page.filter_all_calls()

        visible = (page.is_call_log_visible()
                   or page.is_call_log_empty())
        assert visible, "❌ ALL tab এ ফিরে আসার পর content নেই"

    # ─── TC-106 ─────────────────────────────────────────────────────

    @pytest.mark.skipif_empty_log
    def test_tap_first_call_entry(self, driver):
        """
        TC-106: প্রথম call entry তে tap করা যায়।
        """
        page = CallLogPage(driver)
        page.go_to_recents_tab()

        if page.is_call_log_empty():
            pytest.skip("Call history ফাঁকা — test প্রযোজ্য নয়")

        initial_count = page.get_call_log_count()
        page.tap_first_call_entry()

        # Detail page বা call screen এ গেছে কিনা
        page.press_back()
        current_count = page.get_call_log_count()
        assert current_count == initial_count, \
            "❌ Back করার পর call log count পরিবর্তন হওয়া উচিত নয়"
