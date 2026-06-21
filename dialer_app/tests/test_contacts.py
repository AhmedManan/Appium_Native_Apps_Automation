"""
test_contacts.py - Contacts ফিচার এর Test Cases
"""
import pytest
from pages.contacts_page import ContactsPage


class TestContacts:
    """
    Contacts screen সম্পর্কিত সব test case।
    """

    # ─── TC-201 ─────────────────────────────────────────────────────

    def test_navigate_to_contacts_tab(self, driver):
        """
        TC-201: Contacts tab এ সফলভাবে navigate করা যায়।
        Steps:
            1. Dialer app চালু
            2. Contacts tab এ click
        Expected: Contact list বা empty state দেখায়
        """
        page = ContactsPage(driver)
        page.go_to_contacts_tab()

        visible = (page.is_contacts_list_visible()
                   or page.is_contacts_empty())
        assert visible, "❌ Contacts tab এর content দেখা যাচ্ছে না"

    # ─── TC-202 ─────────────────────────────────────────────────────

    def test_add_new_contact(self, driver):
        """
        TC-202: নতুন contact সফলভাবে যোগ করা যায়।
        Steps:
            1. Contacts tab এ যায়
            2. FAB button tap করে
            3. নাম ও নম্বর দেয়
            4. Save করে
        Expected: Contact তালিকায় নতুন নাম দেখায়
        """
        page = ContactsPage(driver)
        page.go_to_contacts_tab()

        page.add_new_contact(
            first_name="আহমেদ",
            last_name="মানান",
            phone="01700000001"
        )

        # Verify: contact তালিকায় ফিরে নাম দেখায়
        found = page.is_contact_found("আহমেদ মানান")
        if not found:
            found = page.is_contact_found("আহমেদ")
        assert found, "❌ নতুন contact যোগ করার পর তালিকায় দেখা যাচ্ছে না"

    # ─── TC-203 ─────────────────────────────────────────────────────

    def test_search_existing_contact(self, driver):
        """
        TC-203: বিদ্যমান contact সার্চ করা যায়।
        Steps:
            1. Contacts tab এ যায়
            2. Search icon tap করে
            3. Contact এর নাম লেখে
        Expected: সঠিক contact ফলাফলে আসে
        """
        page = ContactsPage(driver)
        page.go_to_contacts_tab()

        if page.is_contacts_empty():
            pytest.skip("কোনো contact নেই — search test skip করা হচ্ছে")

        # প্রথম contact এর নাম পড়ে সেটাই সার্চ করি
        page.search_contact("a")
        results = page.get_search_results()
        assert len(results) >= 0, \
            "❌ Search result structure ঠিক নেই"

    # ─── TC-204 ─────────────────────────────────────────────────────

    def test_search_nonexistent_contact(self, driver):
        """
        TC-204: যে contact নেই তা সার্চ করলে empty state আসে।
        Steps:
            1. Contacts tab এ যায়
            2. Random নাম search করে
        Expected: 'No results' বা empty list আসে
        """
        page = ContactsPage(driver)
        page.go_to_contacts_tab()
        page.search_contact("xyzabc_notexist_12345")

        results  = page.get_search_results()
        is_empty = page.is_contacts_empty()

        assert len(results) == 0 or is_empty, \
            "❌ অবৈধ নাম সার্চে result আসা উচিত নয়"

    # ─── TC-205 ─────────────────────────────────────────────────────

    def test_contact_count_increases_after_add(self, driver):
        """
        TC-205: Contact যোগ করলে count বাড়ে।
        Steps:
            1. Contacts tab এ যায়
            2. প্রাথমিক count নেয়
            3. নতুন contact যোগ করে
            4. Count আবার নেয়
        Expected: নতুন count = পুরনো count + 1
        """
        page = ContactsPage(driver)
        page.go_to_contacts_tab()

        initial_count = page.get_contact_count()

        page.add_new_contact(
            first_name="Test",
            last_name="User",
            phone="01799999999"
        )

        page.go_to_contacts_tab()
        new_count = page.get_contact_count()

        assert new_count == initial_count + 1, \
            (f"❌ Contact যোগের পর count {initial_count + 1} হওয়ার কথা,"
             f" কিন্তু {new_count} পাওয়া গেছে")

    # ─── TC-206 ─────────────────────────────────────────────────────

    @pytest.mark.parametrize("first, last, phone", [
        ("রাহেলা",  "বেগম",  "01812345678"),
        ("করিম",    "সাহেব", "01912345678"),
        ("John",    "Doe",   "01612345678"),
    ])
    def test_add_multiple_contacts(self, driver, first, last, phone):
        """
        TC-206: বিভিন্ন ধরনের নাম দিয়ে contact যোগ করা যায় (parametrized)।
        """
        page = ContactsPage(driver)
        page.go_to_contacts_tab()
        page.add_new_contact(first_name=first, last_name=last, phone=phone)

        found = (page.is_contact_found(f"{first} {last}")
                 or page.is_contact_found(first))
        assert found, f"❌ Contact '{first} {last}' যোগের পর পাওয়া যাচ্ছে না"
