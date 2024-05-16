from tests.pages.api_requests import ApiRequests
import allure


@allure.feature('Создание задачи, подзадачи Jira, списание времени')
def test_create_jira_issue(rand_number_for_entites):
    jira_issue = ApiRequests(rand_number_for_entites)
    jira_issue.create_jira_issue()


@allure.feature('Добавление комментария в задаче Jira')
def test_comment(rand_number_for_entites):
    comment = ApiRequests(rand_number_for_entites)
    comment.comment_issue()


@allure.feature('Создание задачи HD из почты')
def test_create_task_email(rand_number_for_entites):
    task_mail = ApiRequests(rand_number_for_entites)
    task_mail.create_task_email()
    task_mail.check_task_creation()


