from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

class CookieHandler:
    # This method is used to accept the cookies popup
    @staticmethod
    def accept_cookies(driver):
        try:
            accept_button = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "(//a[normalize-space()='Accept All'])[1]")))
            accept_button.click()
        except Exception as e:
            logging.warning(f"No cookie popup found or already accepted. Exception: {e}")
