from tests.pages.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as Ec
from selenium.webdriver.support.wait import WebDriverWait
import configparser
import allure
import time
from selenium.common.exceptions import TimeoutException


create_tsk_btn_selector = (By.XPATH, "//li[@id='create-menu']")
select_prj_selector = (By.XPATH, "//*[@id='project-field']")
summary_selector = (By.XPATH, "//input[@id = 'summary']")
query_field_selector = (By.XPATH, '//*[@id = "customfield_17801-field"]')
span_selector = (By.XPATH, "//div[@class = 'aui-spinner spinner']")
equipment_selector = (By.XPATH, "//strong[text()='Оборудование']")
ke_list_selector = (By.XPATH, "//span[text()='Конфигурационная единица']")
ke_field_selector = (By.XPATH, "//div[@class = 'select2-drop select2-display-none aui-select2-drop aui-dropdown2 select2-with-searchbox aui-layer select2-drop-active']/descendant::input")
ke_option_selector = (By.XPATH, "//li[@class = 'select2-results-dept-0 select2-result select2-result-selectable']")
submit_tsk_selector = (By.XPATH, "//input[@id = 'create-issue-submit']")
task_link_locator = (By.XPATH, "//a[@class = 'issue-created-key issue-link']")


class MainPage(BasePage):
    def __init__(self, browser, rand_number_for_entites):
        super().__init__(browser, rand_number_for_entites)
        self.config = configparser.ConfigParser()
        self.config.read("pytest.ini", encoding="utf-8")
        

    def click_create_task_btn(self):
        with allure.step('Открытие формы создания задачи'):
            time.sleep(2)
            self.find(create_tsk_btn_selector).click()


    @property
    def find_select_prj_field(self):
        self.select_prj = WebDriverWait(self.browser, 59).until(Ec.element_to_be_clickable(select_prj_selector))
        return self.select_prj
        

    def type_scdvs_prj_field(self):
        with allure.step('Выбор проекта "SCDVS"'):
            self.find_select_prj_field.click()
            self.find_select_prj_field.send_keys("SCDVS")
            self.find_select_prj_field.send_keys(Keys.RETURN)
            

    @property 
    def find_summary_field(self):    
        WebDriverWait(self.browser, 15).until(Ec.invisibility_of_element_located(span_selector))   
        self.summary = WebDriverWait(self.browser, 5).until(Ec.element_to_be_clickable(summary_selector))
        return self.summary
        

    def type_summary_prj(self):
        with allure.step('Указание темы задачи'):
            self.find_summary_field.click()
            self.find_summary_field.send_keys("ТестоваяТема" + self.rand_number_for_entities)
            

    @property
    def find_query_field(self):
        self.query_field = WebDriverWait(self.browser, 15).until(Ec.element_to_be_clickable(query_field_selector))
        return self.query_field
       

    def choose_query_type(self):
        with allure.step('Выбор типа запроса'):
            self.find_query_field.click()
            self.find_query_field.send_keys("Запрос на обслуживание")
            time.sleep(1)
            self.find_query_field.send_keys(Keys.RETURN)
            

    def choose_ke(self):
        with allure.step('Указание нового КЕ'):
            self.find(equipment_selector).click()
            self.ke_field_btn = WebDriverWait(self.browser, 15).until(Ec.element_to_be_clickable(ke_list_selector))
            self.ke_field_btn.click()
            self.ke_field = WebDriverWait(self.browser, 20).until(Ec.element_to_be_clickable(ke_field_selector))
            self.ke_field.send_keys("CU.2024." + self.rand_number_for_entities)
            self.ke_option = WebDriverWait(self.browser, 30).until(Ec.presence_of_element_located(ke_option_selector))
            self.ke_option.click()


    def submit_tsk(self):
        with allure.step('Нажатие на кнопку "Создать" форме создания задачи'):    
            WebDriverWait(self.browser, 30).until(Ec.invisibility_of_element_located(span_selector))
            self.submit_tsk_btn = WebDriverWait(self.browser, 15).until(Ec.element_to_be_clickable(submit_tsk_selector))
            self.submit_tsk_btn.click()
            

    def open_task(self):
        with allure.step('Открытие созданной задачи'):
            try:
                self.task_link = WebDriverWait(self.browser, 60).until(Ec.presence_of_element_located(task_link_locator))
                self.task_link.click()
            except TimeoutException:
                self.browser.get(self.config["Jira"]["task_page_url"] + self.rand_number_for_entities)
                
                
    

    
        