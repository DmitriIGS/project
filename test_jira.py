from tests.pages.jira_login_page import LoginPage
from tests.pages.jira_main_page import MainPage
from tests.pages.api_requests import Requests
# from tests.pages.task_page import TaskPage
import allure


@allure.feature('Создание КЕ в БД')
def test_create_ke_api(browser, rand_number_for_entites):
    request = Requests(browser, rand_number_for_entites)
    request.create_new_ke()


@allure.feature('Вход в Jira под внутренней сетью КРОК')
@allure.story('Вход под своим пользователем')
def test_login_jira(browser, rand_number_for_entites):    
    login_page = LoginPage(browser, rand_number_for_entites)
    login_page.open_jira()
    login_page.login_jira()
    

@allure.feature('Создание SCDVS-задачи с созданной КЕ')    
def test_create_scdvs_task(browser, rand_number_for_entites):
    create_task = MainPage(browser, rand_number_for_entites)
    create_task.click_create_task_btn()
    create_task.type_scdvs_prj_field()
    create_task.type_summary_prj()
    create_task.choose_query_type()
    create_task.choose_ke()
    create_task.submit_tsk()
    create_task.open_task()


# def test_check_scdvs_task_fields(browser, rand_number_for_entites):
#     scdvs_task = TaskPage(browser, rand_number_for_entites)
#     scdvs_task.open_task()