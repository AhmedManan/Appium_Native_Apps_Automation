from ..conftest import driver
from ..pages.download_page import DownloadPage


class TestDownloadPage:

    def test_title_verification(self, driver):
        driver = driver
        self.download_page = DownloadPage(driver)
        assert self.download_page.get_heading_text() == "Downloads"

    def test_header_elements(self, driver):
        driver = driver
        self.download_page = DownloadPage(driver)
        assert self.download_page.verify_header_elements()

    def test_header_root_button_functionality(self, driver):
        driver = driver
        self.download_page = DownloadPage(driver)
        assert self.download_page.check_header_root_button_functionality()

    def test_header_search_functionality(self, driver):
        driver = driver
        self.download_page = DownloadPage(driver)
        assert self.download_page.check_header_search_accessibility(search_text="no match")
        assert self.download_page.message_text == "No matches in Downloads"

    def test_more_options_accessibility(self, driver):
        driver = driver
        self.download_page = DownloadPage(driver)
        assert self.download_page.check_more_options_accessibility()