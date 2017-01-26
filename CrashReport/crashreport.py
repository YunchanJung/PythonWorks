# requirement
#
# python3.6
# selenum python lib 설치 필요
# chromedriver 구글링 후 다운로드, 현재 경로에 추가할 것

import pip
from selenium import webdriver
import datetime
import time

class Project:
    nds_node_id = ""
    nelo_project_name = ""
    phase = ""

    def __init__(self, project_name, node_id, phase):
        self.nds_node_id = node_id
        self.nelo_project_name = project_name
        self.phase = phase

## user settings ##
webDriverPath = './chromedriver'

## project settings ##
project_list = [
    Project("blog_android", "100116562", "real"),
    Project("blog_ios", "100116563", "REAL"),
    Project("post_android", "100245522", "real"),
    Project("post_ios", "100245523", "real")
]


def install(package):
    pip.main(['install', package])

if __name__ == '__main__':
    install('selenium')

def input_id_pw():
    id = input("id:")
    pw = input("pw:")
    return (id, pw)


def login(driver, id, pw):
    url = "https://nss.navercorp.com/loginRequest?serviceId=NDS&targetUrl=http%3A%2F%2Fnds.navercorp.com%2F"
    driver.get(url)

    input_id = driver.find_element_by_id("user_id")
    input_id.send_keys(id)

    input_pw = driver.find_element_by_id("user_pw")
    input_pw.send_keys(pw)

    input_pw.submit()


def getStartDate():
    today = datetime.date.today()
    next_monday = today + datetime.timedelta(days=-today.weekday(), weeks=1)
    return next_monday - datetime.timedelta(14)     #14일전 날짜 구하기


def getUB(driver, service_node_id, start_date):
    ub_url = "http://nds.navercorp.com/index.php?node_id=%s&period_pick=weekly&start_date=%s&main_menu=service&sub_menu=summary&left_menu=&sort_by=&period_opt=" % (service_node_id, start_date)
    driver.get(ub_url)
    td = driver.find_element_by_css_selector("tr.first.high > td:nth-child(3)")
    return td.text

def login_nelo(driver, id, pw):
    url = "http://nelo2.navercorp.com/login?url=%2F"
    driver.get(url)
    time.sleep(2)

    input_id = driver.find_element_by_name("username")
    input_id.send_keys(id)

    input_pw = driver.find_element_by_name("password")
    input_pw.send_keys(pw)

    input_pw.submit()
    time.sleep(2)


def getTimeStamp(date1):
    strd = date1.strftime("%d/%m/%Y")
    return time.mktime(datetime.datetime.strptime(strd, "%d/%m/%Y").timetuple())


def getCrash(driver, project_name, phase, start_date):
    start_time_stamp = str(getTimeStamp(start_date))[:9] + "0000"
    end_time_stamp = str(getTimeStamp(start_date + datetime.timedelta(7)))[:9] + "0000"

    query_url = "http://nelo2.navercorp.com/search?cmd=projectName%3A%22" + project_name + "%22%20AND%20logLevel%3A%22FATAL%22%20AND%20phase.raw%3A%22" + phase + "%22&st=" + start_time_stamp + "&et=" + end_time_stamp
    driver.get(query_url)
    time.sleep(5)

    count = driver.find_element_by_id("logsCount")
    count_text = str(count.text)
    count_text = count_text.split()[0]
    return count_text

def print_date(start_date):
    end_date = start_date + datetime.timedelta(6)
    print(start_date, "~", end_date)


def getPercent(crash, ub):
    crash_num = (int)(crash.replace(',',''))
    ub_num = (int)(ub.replace(',',''))
    return str(round(crash_num / ub_num * 100, 2))


## main ##



idpw = input_id_pw()
id = idpw[0]
pw = idpw[1]
print("")

print("안녕하세요 정윤찬 입니다.")
driver = webdriver.Chrome(webDriverPath)
print("")

start_date = getStartDate()
print_date(start_date)

login(driver, id, pw)
login_nelo(driver, id, pw)

for project in project_list:
    print(project.nelo_project_name)

    crash = getCrash(driver, project.nelo_project_name, project.phase, start_date)
    ub = getUB(driver, project.nds_node_id, start_date)
    print("Crash %s / UB %s = " % (crash, ub) + getPercent(crash, ub) + "%")
    print("")

driver.quit()
print("감사합니다.")
