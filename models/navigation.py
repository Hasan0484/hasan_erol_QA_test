from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from models.cookie_handler import CookieHandler

class Navigation:
    def __init__(self):
        # Ensure ChromeDriver is installed and set up correctly
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service)        
                
    # Open and Close the URL
    def open_url(self, url):
        self.driver.get(url)
        CookieHandler.accept_cookies(self.driver)
        self.driver.maximize_window()

    def close(self):
        self.driver.quit()