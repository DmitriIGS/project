from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement



class BasePage:
    def __init__(self, browser: webdriver.Chrome, 
                rand_number_for_entites: str):
        self.browser = browser
        self.rand_number_for_entities = rand_number_for_entites

    
    def find(self, args) -> WebElement:
        return self.browser.find_element(*args)
   
    
    
