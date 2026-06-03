from appium.webdriver.common.appiumby import AppiumBy


class DownloadPage:
    page_heading_xpath="(//*[@text='Downloads'])[2]"
    header_toolbar_xpath= '//*[@content-desc="Show roots"]'
    header_search_accessibility_id= "Search"
    more_options_accessibility_id= 'More options'

    root_toolbar_heading_id='roots_toolbar'
    root_toolbar_list_id = "roots_list"

    search_textfield_id= "search_src_text"
    message_id = 'message'
    message_text : str # No matches in Downloads

    new_window_option_xpath = '//android.widget.TextView[@resource-id="com.google.android.documentsui:id/title" and @text="New window"]'

    def __init__(self, driver):
        self.driver = driver

    def get_heading_text(self):
        heading_text = self.driver.find_element(AppiumBy.XPATH, self.page_heading_xpath).text
        return heading_text

    def verify_header_elements(self):
        # Store the boolean result of each check
        toolbar_displayed = self.driver.find_element(AppiumBy.XPATH, self.header_toolbar_xpath).is_displayed()
        search_displayed = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, self.header_search_accessibility_id).is_displayed()
        options_displayed = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, self.more_options_accessibility_id).is_displayed()
        heading_displayed = self.driver.find_element(AppiumBy.XPATH, self.page_heading_xpath).is_displayed()

        # Return True only if ALL are True
        return toolbar_displayed and search_displayed and options_displayed and heading_displayed

    def check_header_root_button_functionality(self):
        clickable = self.driver.find_element(AppiumBy.XPATH, self.header_toolbar_xpath).is_enabled()
        self.driver.find_element(AppiumBy.XPATH, self.header_toolbar_xpath).click()
        toolbar_heading_displayed = self.driver.find_element(AppiumBy.ID, self.root_toolbar_heading_id).is_displayed()
        toolbar_list_displayed = self.driver.find_element(AppiumBy.ID, self.root_toolbar_list_id).is_displayed()
        self.driver.back()

        return clickable and toolbar_heading_displayed and toolbar_list_displayed

    def check_header_search_accessibility(self, search_text:str):
        clickable = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, self.header_search_accessibility_id).is_enabled()
        self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, self.header_search_accessibility_id).click()
        self.driver.find_element(AppiumBy.ID, self.search_textfield_id).send_keys(search_text)
        self.driver.find_element(AppiumBy.ID, self.message_id).is_displayed()
        self.message_text = self.driver.find_element(AppiumBy.ID, self.message_id).text

        return clickable

    def check_more_options_accessibility(self):
        clickable = self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, self.more_options_accessibility_id).is_enabled()
        self.driver.find_element(AppiumBy.ACCESSIBILITY_ID, self.more_options_accessibility_id).click()
        option_displayed=self.driver.find_element(AppiumBy.XPATH, self.new_window_option_xpath).is_displayed()
        self.driver.back()

        return clickable and option_displayed