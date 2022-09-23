from cgi import print_arguments
import time
import os
import random
from unittest import result
import pyperclip
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, NoSuchElementException, InvalidSessionIdException
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

'''
seleniu version 4.4.3
python version 3.7

'''

def main() :

    driver = setDriver('./chromedriver.exe', setChromeOpt())

    """
    수집하기
    """
    
    # 사이트 url
    # site_url = 'https://m19.kotbc.com/'
    site_url = 'https://www.naver.com/'


    '''
    영화 : 장르, 제목, 배급사, 감독, 등급, 주연, 조연, 줄거리, 재생시간, 개봉일
    방송 : 장르, 제목, 편성, 제작사, 연출, 등급, 주연, 줄거리, 방영일, 종영여부, 총회차
    '''
    
    
    # 맨처음 키워드 입력 셀렉터
    first_input_keyword_selector = 'div.green_window input.input_text'
    
    # 다음 키워드 입력 셀렉터
    next_input_keyword_selector = 'div.greenbox input.box_window'
    
    # 돋보기 셀렉터
    search_button_selctor = 'div.search_area button.btn_submit'
    
    # 정보 셀렉터
    information_list_selector='div ul.tab_list li.tab_tab'
   

    # 대기시간
    d_time = 5
 
 
    # 검색창에 맨처음 키워드 입력
    # driver.find_element_by_name("query").send_keys('창궐')
    driver.find_element('name', "query").send_keys('창궐')
    
    # 돋보기 클릭
    clickElementIdx(driver, search_button_selctor)
    
    
    
    # 정보 리스트에서 요소 가져오기
    information_list=getElement(driver,information_list_selector)
    
    # 정보 리스트 1, 2번 요소
    for table_index in range(information_list[1],information_list[2]):
        
        # 정보 테이블에서 정보 요소 클릭
        clickElementIdx(driver,information_list_selector,table_index)
        
        
'''
    # 기록할 txt 파일 오픈 
    f = wLog (None, '--- 크롤링 시작 ---' ,'', enter = 2, flag='open')

    # 해당 사이트로 이동
    getUrl(driver, site_url, d_time)
    
    print('<<<<<<<<<<'+'영화 크롤링'+'>>>>>>>>>>')
    
    # 검색창으로 이동
    getElement(driver, first_input_keyword_selector)        
    
     
    
    
    
                        
    # 검색창에 다음 키워드 입력
    driver.find_element_by_name("nx_query").send_keys('무지개')
                    
                    
                    
                    
                    
    wLog(f, '----- 채증 완료. -----', '', enter=2, flag='close')
'''




# Chrome Driver Option Setting
def setChromeOpt (headless = True) :

    chrome_options = Options()
    # 창 없이 크롤링
    # if headless :
    #     chrome_options.add_argument("headless")

    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument("--start-maximized")        
    chrome_options.add_argument('--ignore-ssl-errors')
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-setuid-sandbox")
    chrome_options.add_argument("--disable-blink-features")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")      
    chrome_options.add_argument("force-device-scale-factor=1")
    chrome_options.add_argument("high-dpi-support=1")
    chrome_options.add_argument("loggingPrefs=performance1")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36")
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_argument("--force-renderer-accessibility")

    #창 크기 조절
    chrome_options.add_argument("window-size=2560,1440")

    return chrome_options

# Driver
def setDriver (driverPath, option) :
    driver = webdriver.Chrome(executable_path = driverPath, desired_capabilities=DesiredCapabilities.CHROME, chrome_options=option)
    return driver


# 엘리먼트 요소 가져오기
def getElement (driver, selector, parent= None, list = True):

    if parent :
        driver = parent
    
    # 셀랙터로 요소 배열 get
    if list :
        element = driver.find_elements(by=By.CSS_SELECTOR, value=selector)
    else :
    # 셀랙터로 첫번째 요소 get
        element = driver.find_element(by=By.CSS_SELECTOR, value=selector)

    return element

# 해당 엘리먼트의 n번째 요소 가져와서 클릭
def clickElementIdx (driver, selector, idx):
    getElement(driver, selector, list=True)[idx].click()


# 해당 요소 속성값 가져오기
def getAttr (element = None , selector = [],  attr='text'):

    # selector를 인자로 받는 경우 추가
    if element is None :
        element = getElement( selector[0], selector[1] , list=False) # driver, selector

    if attr == 'text' :
        result = element.text
    else :
        result = element.get_attribute(attr)
    return result

# 현재 창에서 url로 이동
def getUrl(driver, url, d_time = 10):
    driver.get(url)
    time.sleep(d_time)

# 새탭으로 오픈
def openNewTab (driver, attr, d_time = 10) :
    # get url 
    url = attr.get_attribute('href')

    #새탭열기
    driver.execute_script(f'''
    window.open("{url}","width="+screen.availWidth+",height="+screen.availHeight);            
    ''')
    window_handles = driver.window_handles
    driver.switch_to.window(window_handles[-1])
    driver.implicitly_wait(d_time)

    return url

# 새창으로 오픈
def openNewWindow (driver, attr, d_time = 10) :
    # get url 
    url = attr.get_attribute('href')

    #새창열기
    driver.execute_script(f'''
    window.open("{url}","PopupWin","width="+screen.availWidth+",height="+screen.availHeight);            
    ''')
    window_handles = driver.window_handles
    driver.switch_to.window(window_handles[-1])
    driver.implicitly_wait(d_time)

    return url

# 마지막으로 연 창을 닫음
def closeCurrentWindow (driver) :
    driver.close()
    window_handlers = driver.window_handles
    driver.switch_to.window(window_handlers[-1])

# print, txt 기록
def wLog (file, message='' ,txt='', enter = 1, flag = None):
    
    if flag == 'open' :
        file = open('data/log.txt', 'a')

    newline = '\n'*enter
    print(f"[{time.time()}]{message} : {txt} {newline}", end='')
    file.write(f"{message} : {txt} {newline}")

    if flag == 'close' :
        file.close()

    return file


if __name__ == '__main__':

    main()
