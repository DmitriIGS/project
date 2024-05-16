import requests as r
import configparser
from requests.auth import HTTPBasicAuth
import allure
import imaplib
import cx_Oracle
import time 
from datetime import datetime
import json
from typing import Literal


class ApiRequests:
    def __init__ (self, rand_number_for_entities):
        self.rand_number_for_entities = rand_number_for_entities
        self.config = configparser.ConfigParser()
        self.config.read('pytest.ini', encoding="utf8")
        self.result_db = []
        self.email_sender_password = self.config['Api']['email_sender_password']
        self.api_ke_url = self.config['Api']['api_ke_url']
        self.xml_ke = self.config['Api']['xml_ke']
        self.apilogin = self.config['Api']['apilogin']
        self.apipassword = self.config['Api']['apipassword']
        self.email_sender = self.config['Api']['email_sender']
        self.email_box_ip = self.config['Api']['email_box_ip']
        self.worklog_url = self.config['Api']['worklog_url']
        self.dbuser = self.config['DB']['dbuser']
        self.dbpassword = self.config['DB']['dbpassword']
        self.dsn = self.config['DB']['dsn']
        self.new_issue_url = self.config['Api']['new_issue_url']
        self.comment_url = self.config['Api']['comment_url']
        self.issue = json.loads(self.config['Api']['issue_json'])
        self.subtask = json.loads(self.config['Api']['subtask_json'])
        self.worklog = json.loads(self.config['Api']['worklog_json'])
        self.scdvs_task = json.loads(self.config['Api']['scdvs_task_json'])
        self.query_worklog = str(self.config["DB"]["query_worklog"])
        self.query_issue = str((self.config["DB"]["query_issue"]))
        self.current_date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        self.current_date_db = datetime.now().strftime("%d.%m.%Y")
        self.oracle_client = self.config['DB']['oracle_client']
        # self.comment = json.loads(self.config['Api']['comment'])
        # self.comment_json = json.dumps(self.comment)
        # self.comment_ = json.loads(self.config['Api']['comment'])
        self.comment_json = self.config['Api']['comment']


    def db_init_oracle_client(self):
        cx_Oracle.init_oracle_client(lib_dir=self.oracle_client)


    def sql_query(self, query: str, key) -> bool:

        self.con = cx_Oracle.connect(user=self.dbuser, password=self.dbpassword, dsn=self.dsn)
        self.cursor = self.con.cursor()
        self.cursor.execute(query.format(key))
        for row in self.cursor.fetchall():
            self.result_db.append(row)
        self.cursor.close()
        self.con.close()

        return len(self.result_db) > 0
    

    def create_entity(self, url, data, apptype: Literal["xml", "json"]):
        self.response = r.post(url, 
                               data=data, 
                               auth=HTTPBasicAuth(self.apilogin, self.apipassword), 
                               verify=False, 
                               headers={'Content-type': f'application/{apptype}'})
        assert self.response.status_code == 200 or 201
        return self.response


    def check_task_creation(self) -> bool:
        self.con = cx_Oracle.connect(user=self.dbuser, password=self.dbpassword, dsn=self.dsn)
        self.cursor = self.con.cursor()
        prev_time = time.time() + 120
        now_time = time.time() 
        result = False
        while now_time <= prev_time:
            time.sleep(10)
            self.cursor.execute(self.query_issue.format('199802'))
            for row in self.cursor.fetchall():
                self.result_db.append(row)
            if len(self.result_db) > 0 and self.result_db[1] == self.current_date_db:
                result = True
                break
            now_time = time.time()

        self.cursor.close()
        self.con.close()     
        assert result is True


    def create_jira_issue(self):
        with allure.step("Создание задачи JIRA"):
            issue_json = json.dumps(self.issue, ensure_ascii=False)
            self.create_entity(self.new_issue_url, issue_json, "json")
            api_task_response = json.loads(self.response.content)
            self.create_jira_subtask(api_task_response)
            self.create_worklog(api_task_response)
            

    def create_jira_subtask(self, api_task_response):
        with allure.step("Создание подзадачи"):  
            self.subtask['fields']['parent']['key'] = api_task_response['key']
            subtask_json = json.dumps(self.subtask, ensure_ascii = False)
            self.create_entity(self.new_issue_url, subtask_json, "json")


    def create_worklog(self, api_task_response):
        with allure.step("Списание времени"):
            self.worklog['workStart'] = self.current_date + "+0300"
            self.worklog['issueKey'] = api_task_response['key']
            worklog_json = json.dumps(self.worklog, ensure_ascii = False)
            self.worklog_response = self.create_entity(self.worklog_url, worklog_json, "json")
            # parsed_worklog_response = json.loads(self.worklog_response.content)
            # self.worklog_sync(parsed_worklog_response)


    # Закомментирована, т.к. таблица пока не показывает актуальный результат интеграции по списанию времени
    # def worklog_sync(self, parsed_worklog_response):
    #     with allure.step("Интеграция по списанию времени"):
    #         self.sql_query(self.query_worklog, parsed_worklog_response['id'])

        
    def comment_issue(self):
        self.create_entity(self.comment_url, self.comment_json, "json")
            

    def create_new_ke(self):
        self.create_entity(self.api_ke_url, self.xml_ke.format(self.rand_number_for_entities), "xml")


    def create_task_email(self):
        self.username = self.email_sender
        self.password = self.email_sender_password
        self.mail_server = self.email_box_ip
        self.imap_server = imaplib.IMAP4_SSL(host=self.mail_server, port=993)
        self.imap_server.login(self.username, self.password)

        self.imap_server.select('inbox')
        self.search_criteria = None
        
        self.status, self.results = self.imap_server.search(self.search_criteria, '(FROM "dlazutin@croc.ru" SUBJECT "jiraTestHD199802")') #?
        self.imap_server.store(self.results[0], '-FLAGS', '\SEEN')

        self.imap_server.logout()


