from datetime import date, datetime, timezone

import configparser
import json
import requests as r
import logger
from requests.auth import HTTPBasicAuth
import pymsteams
import cx_Oracle


config = configparser.ConfigParser()
config.read('pytest.ini', encoding="utf8")


api_ke_url = config['Api']['api_ke_url']
xml_ke = config['Api']['xml_ke']
apilogin = config['Api']['apilogin']
apipassword = config['Api']['apipassword']
email_sender = config['Api']['email_sender']
email_sender_password = '%csc6i?*SS12345'
email_reciever = config['Api']['email_reciever']
email_box_ip = config['Api']['email_box_ip']
worklog_url = config['Api']['worklog_url']
dbuser = config['DB']['dbuser']
dbpassword = config['DB']['dbpassword']
dsn = config['DB']['dsn']
new_issue_url = config['Api']['new_issue_url']
comment_url = config['Api']['comment_url']

issue = json.loads(config['Api']['issue_json'])
subtask = json.loads(config['Api']['subtask_json'])
worklog = json.loads(config['Api']['worklog_json'])
scdvs_task = json.loads(config['Api']['scdvs_task_json'])

query_worklog = str(config["DB"]["query_worklog"])
query_issue = str((config["DB"]["query_issue"]))

current_date = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


# note = worklog_json.format(today, current_time)

# scdvs = '{ "fields": { "project": { "key": "SCDVS" }, "summary": "TestScdvs",  "issuetype": { "id": "13309" }, "customfield_17801": "Инцидент" } }'
# new = '{' + note + '}'

# url = 'https://jira-pr.croc.ru/rest/api/2/issue/'

# new_subtask_json = subtask_json 

# def create_worklog():
#         try:
#             response = r.post(
#                 worklog_url, data = new, auth = HTTPBasicAuth(apilogin, apipassword), verify = False, headers = {'Content-type': 'application/json'})
#             print (response.status_code) 
#         except Exception as e:
#             logger.error('Не удалось списать время по задаче ', e)

# create_worklog()


# def create_scdvs_task():
#     try:
#         response = r.post(new_issue_url, json= data, auth = HTTPBasicAuth(apilogin, apipassword), verify = False, headers={'Content-Type': 'application/json'})
#         # assert response.status_code == 201
#         print(response.status_code)
#     except Exception as e:
#         logger.error('Не удалось создать задачу ', e)


# create_scdvs_task()

# def create_entity():
#         response = r.post(
#         comment_url, data = {"body": "Test"}, auth = HTTPBasicAuth(apilogin, apipassword), verify = False, headers = {'Content-type': 'application/json'})
        
#         print(response)
        
# create_entity()

# myTeamsMessage = pymsteams.connectorcard("<Microsoft Webhook URL>")
# myTeamsMessage.text("this is my text")
# myTeamsMessage.send()

def sql_query() -> bool:
        cx_Oracle.init_oracle_client(lib_dir=r"C:\Users\DLazutin\Downloads\instantclient_21_13")
        con = cx_Oracle.connect(user = dbuser, password = dbpassword, dsn = dsn)
        cursor = con.cursor()
        cursor.execute("update AO_10A4CE_CROC_ACTIVITY set time_loss_clarity = 0 where croc_proj_code = 'A1601105'")

        cursor.close()
        con.close()

sql_query()