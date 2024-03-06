from tests.pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as Ec
from selenium.webdriver.support.wait import WebDriverWait
import configparser

# class TaskPage(BasePage):
#     def __init__(self, browser, rand_number_for_entites):
#         super().__init__(browser, rand_number_for_entites)
    
#     def open_task(self): 
#         config = configparser.ConfigParser()
#         config.read("pytest.ini")
#         self.browser.get(config["Jira"]["task_page_url"] + self.rand_number_for_entities)