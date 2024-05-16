from tests.pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as Ec
from selenium.webdriver.support.wait import WebDriverWait
import configparser


equipmentBtn_selector = (By.XPATH, "//strong[text()='Оборудование']")
agreementNum_selector = (By.XPATH, "//div[@id = 'customfield_20357-val']")
serialNum_selector = (By.XPATH, "//div[@id = 'customfield_20300-val']")
keName_selector = (By.XPATH, "//div[@id = 'customfield_20359-val']")
partNum_selector = (By.XPATH, "//div[@id = 'customfield_20301-val']")


class TaskPage(BasePage):
    def __init__(self, browser, rand_number_for_entites):
        super().__init__(browser, rand_number_for_entites)
        self.config = configparser.ConfigParser()
        self.config.read('pytest.ini', encoding="utf8")


    @property
    def find_agreementNum(self):
        self.agreementNum = WebDriverWait(self.browser, 15).until(Ec.element_to_be_clickable(agreementNum_selector))
        return self.agreementNum


    def check_agreementNUm(self):
        assert self.find_agreementNum.text == self.config["TaskPage"]["agreementNum"]
    

    def click_equipmentBtn(self):
        self.find(equipmentBtn_selector).click()
    

    def check_serialNum(self):
        assert self.find(serialNum_selector).text == self.config["TaskPage"]["serialNum"]

    
    def check_keName(self):
        assert self.find(keName_selector).text == self.config["TaskPage"]["keName"]


    def check_partNum(self):
        assert self.find(partNum_selector).text == self.config["TaskPage"]["partNum"]