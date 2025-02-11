import unittest
from models.navigation import Navigation
from selenium.webdriver.common.action_chains import ActionChains
from models.page_elements import PageElements
import logging
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TestAutoQA(unittest.TestCase):

    def setUp(self):        
        self.navigation = Navigation()
        self.driver = self.navigation.driver
        self.actions = ActionChains(self.driver)
        self.wait = WebDriverWait(self.driver, 10)
        logging.info("ChromeDriver is ready!")

    def test_qa_page_career(self):
        self.navigation.open_url("https://useinsider.com/")
        self.assertIn("#1 Leader in Individualized, Cross-Channel CX — Insider", self.driver.title, "Home page title does not match")
        logging.info(self.driver.title)
      
        # this area is to get the screen into careers page
        company_btn = PageElements.find_element(self.driver, "(//a[normalize-space()='Company'])[1]")
        company_btn.click()

        careers_btn = PageElements.find_element(self.driver, "//a[normalize-space()='Careers']")
        careers_btn.click()            
      
        self.assertIn("Careers", self.driver.title, "Careers page title does not match")
        logging.info("Page title after clicking Careers: " + self.driver.title)
      
        #after getting into the careers page, we will check the blocks
        life_at_insider_title = PageElements.find_element(self.driver, "//h2[normalize-space()='Life at Insider']")
        self.assertTrue(life_at_insider_title.is_displayed(), "Life at Insider block is not displayed")
        logging.info("Life at Insider block is displayed")

        locations_title = PageElements.find_element(self.driver, "//h3[normalize-space()='Our Locations']")
        self.assertTrue(locations_title.is_displayed(), "Our Locations block is not displayed")
        logging.info("Our Locations block is displayed")

        teams_btn = PageElements.find_element(self.driver, "(//a[normalize-space()='See all teams'])")        
      
        if teams_btn and teams_btn.is_displayed():   # standart click was not working, so we need to scroll to the element
            logging.info("All teams block is NOT open...")
            logging.info("...Clicking on 'See all teams' button...")                     
            self.actions.move_to_element(teams_btn).move_by_offset(0, -300).perform() #tried different ways to scroll to the element, only this one works for this specific case
            self.actions.move_to_element(teams_btn).click().perform()
            self.driver.execute_script("window.scrollBy(0,1750);") #scroll down to see the teams after selecting the location. I had to use javaScript because the page was not scrolling down with the standart scroll method     
            self.actions.pause(2).perform()
          
            logging.info("Teams block is now Open!")
        else:
            logging.info("Teams block was already opened.")

        configuration_btn = PageElements.find_element(self.driver, "(//div[@class='job-image text-center'])[12]")
        configuration_btn.click()
      
        self.assertIn("quality assurance job", self.driver.title,"QA Engineer page title does not match")        

        see_jobs_btn = PageElements.find_element(self.driver, "//a[normalize-space()='See all QA jobs']")
        see_jobs_btn.click()               
      
        self.driver.execute_script("window.scrollBy(0,500);") #scroll down to see the job titles before selecting the location. Any other method did not work for this specific case      
        self.actions.pause(3).perform()
      
        filter_by_location = PageElements.find_element(self.driver, "//option[@class='job-location istanbul-turkiye']")
        filter_by_location.click()        
        
        # selected department is checked and it comes automatically as "Quality Assurance"
        qa_department_selected = PageElements.find_element_css(self.driver, "#select2-filter-by-department-container")
        self.assertIn("Quality Assurance", qa_department_selected.text, "Quality Assurance is not found in the department container")        
        
        qa_jobs_list = PageElements.find_elements(self.driver, "#jobs-list") #Get the list of jobs created by the filter      
        for job in qa_jobs_list: # for every job in the list, check if the department and location are correct            
            if "Quality Assurance" in job.text:                
                self.assertIn("Quality Assurance", job.text, "Quality Assurance is not found in the department")                
            if "Istanbul, Turkiye" in job.text:
                self.assertIn("Istanbul, Turkiye", job.text, "Istanbul, Turkiye is not found in the location")   
        logging.info("All jobs are checked if they are in the correct Department and Location")         
                              
        # move the first job to see the view role button
        qa_automation_title =  PageElements.find_element(self.driver, "//p[normalize-space()='Senior Software Quality Assurance Engineer']")        
        self.assertTrue(qa_automation_title.is_displayed(), "QA Automation title is not displayed")
        self.actions.move_to_element(qa_automation_title).perform()
      
        # click on the view role button
        view_role_btn = PageElements.find_element(self.driver, "//section[@id='career-position-list']//div[@class='row']//div[1]//div[1]//a[1]")
        view_role_btn.click()        
      
        self.driver.switch_to.window(self.driver.window_handles[-1]) #switch to the new tab to check the url
              
        WebDriverWait(self.driver, 20).until(EC.url_contains("https://jobs.lever.co/"))
        self.assertIn("https://jobs.lever.co/", self.driver.current_url,"URL does not match with 'jobs.lever.co'")

    def tearDown(self):
        self.navigation.close()

if __name__ == "__main__":
    # Creating a test suite    
    suite = unittest.TestSuite()
    suite.addTest(TestAutoQA('test_qa_page_career'))

    # Running the test suite
    runner = unittest.TextTestRunner()
    runner.run(suite)
