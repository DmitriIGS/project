from tests.pages.base_page import BasePage
from selenium.webdriver.common.by import By
import configparser
import allure


login_btn_selector = (By.XPATH, '//*[@id="split-auth-sso"]/a')


class LoginPage(BasePage):
    def __init__(self, browser, rand_number_for_entites):
        super().__init__(browser, rand_number_for_entites)
        self.config = configparser.ConfigParser()
        self.config.read("pytest.ini", encoding="utf-8")


    def open_jira(self):
        with allure.step('Открытие Jira'): 
            self.browser.get(self.config["Jira"]["jira_login_page_url"])
            
    
    def login_jira(self):
        self.find(login_btn_selector).click()
        

    
   

    
        