import requests as r
import configparser
from requests.auth import HTTPBasicAuth
from tests.pages.base_page import BasePage
import logger
import allure


class Requests(BasePage):
    @allure.feature('Создание КЕ в БД')
    def __init__(self, browser, rand_number_for_entites):
        super().__init__(browser, rand_number_for_entites)


    def create_new_ke(self):
        try:
            config = configparser.ConfigParser()
            config.read('pytest.ini')

            api_ke_url = config['Api']['api_ke_url']
            xml_ke = config['Api']['xml_ke']
            apilogin = config['Api']['apilogin']
            apipassword = config['Api']['apipassword']

            self.response = r.post(
                api_ke_url, data=(xml_ke.format(self.rand_number_for_entities)), auth = HTTPBasicAuth(apilogin, apipassword), verify = False)
            assert self.response.status_code == 200
        except Exception as e:
            logger.error('Не отправить http-запрос для создания КЕ ', e)
            self.browser.quit()