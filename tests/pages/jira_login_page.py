from tests.pages.base_page import BasePage
from selenium.webdriver.common.by import By
import configparser
import logger
import allure


login_btn_selector = (By.XPATH, '//*[@id="split-auth-sso"]/a')
create_tsk_btn_selector = (By.XPATH, "//li[@id='create-menu']")


class LoginPage(BasePage):
    def __init__(self, browser, rand_number_for_entites):
        super().__init__(browser, rand_number_for_entites)
    

    def open_jira(self):
        with allure.step('Открытие Jira'):
            try: 
                config = configparser.ConfigParser()
                config.read("pytest.ini")
                self.browser.get(config["Jira"]["jira_login_page_url"])
            except Exception as e:
                logger.error('Не удалось открыть страницу для входа в Jira ', e)
                self.browser.quit()

    
    def login_jira(self):
        try:
            self.find(login_btn_selector).click()
        except Exception as e:
            logger.error('Не найдена кнопка входа под своим сотрудником в Jira ', e)
            self.browser.quit()

    
   

    
        