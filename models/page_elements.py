from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import logging

class PageElements:
    # This class is created to handle the page elements in a more structured way
    @staticmethod
    def find_element(driver, element_xpath):
        try:
            element = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, element_xpath)))
            return element
        except Exception as e:
            logging.error(f"Object: {element_xpath} not found. Exception: {e}")
            return None
            
    @staticmethod
    def find_element_css(driver, element_css):
        try:
            element = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, element_css)))
            return element
        except Exception as e:
            logging.error(f"Object: {element_css} not found. Exception: {e}")
            return None
        
    @staticmethod
    def find_elements(driver, element_css):
        try:
            element = WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.CSS_SELECTOR, element_css)))
            return element
        except Exception as e:
            logging.error(f"Object: {element_css} not found. Exception: {e}")
            return None