from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import ElementNotVisibleException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
from core.utils.cookies import load_cookie,save_cookie
from core.utils.loader import get_path
import pickle


options = Options()
# options.add_experimental_option("excludeSwitches", ["enable-automation"])
# options.add_experimental_option('useAutomationExtension', False)


options.headless = True
options.add_experimental_option('excludeSwitches', ['enable-logging'])

driver = webdriver.Chrome(executable_path=get_path("driver" , "chromedriver.exe"), options= options)
# driver.maximize_window()
driver.implicitly_wait(10)


class Linkedin(object):

    def __init__(self , username , password, login_url, linkedin_url, search_quarry ,
                    location_quarry, current_page, last_page):

        self.username = username
        self.password = password
        self.login_url = login_url
        self.linkedin_url = linkedin_url
        self.search_quarry = search_quarry
        self.location_quarry = location_quarry
        self.current_page = current_page
        self.last_page = last_page


    def user_login(self):
        try: 
            driver.get(self.login_url)
            try:
                username_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR , "#username"))
                ).send_keys(self.username)

                password_element = WebDriverWait(driver , 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "#password"))
                )

                if password_element is not None:
                    password_element.send_keys(self.password)

                    """
                    For login btn element
                    """
                    login_btn_element = WebDriverWait(driver , 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".mercado-button--primary"))
                    )
                    
                    if login_btn_element is not None:
                        login_btn_element.click()
                        print("You are successfully loggedin...!!!")
                        save_cookie(driver, get_path("cookies", "cookies.txt"))
                        print("cookies saved successfully in 'cookie' folder")


                    else:
                        print("Login button element is not located")
                
                else: 
                    print("Password element is not located")
            
            except ElementNotVisibleException as e:
                print(e)
        except TimeoutException as e:
            print("Oops!! Time out.")


    def load_credentials(self):
        driver.get(self.linkedin_url)
        load_cookie(driver, get_path("cookies" , "cookies.txt"))
        driver.refresh()


    def accept_invitaions(self):
        """
        To accept user invitation request to connect with them.
        https://www.linkedin.com/mynetwork/
        
        """
        self.load_credentials()       
        try:
            driver.get("https://www.linkedin.com/mynetwork/")
            try:
                time.sleep(5)

                """
                Collepsing the pop up chat message box
                """
                msg_popup = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH , "//*[@id='msg-overlay']/div[1]/header"))
                )
                print(msg_popup)
                msg_popup.click()
                
                """
                output of invitation seder name list 
                """
                total_invitation = 0
                total_accepted_invitation = 0 
                get_list = driver.find_elements_by_xpath("//div[@class='ember-view']/ul/li[@class='invitation-card artdeco-list__item ember-view']")
                if get_list is not None:
                    time.sleep(5)
                    for name in get_list:
                        get_name_element = name.find_elements_by_xpath(".//div[@class='display-flex ph2 pt1 pb1']/div/div/a/span[@class='invitation-card__title t-16 t-black t-bold']")
                        for name in get_name_element:
                            name = name.text 
                            print("Invitation sender name :", name)
                            total_invitation +=1
                            time.sleep(5)
                    print("You have total invitation request ===>", total_invitation)
                    time.sleep(1)
                    """
                    Accept invitaions
                    """
                    for accept_btn in get_list:
                        get_accept_btns = accept_btn.find_elements_by_xpath(".//div/div[@class='invitation-card__action-container pl3']/button[@class='invitation-card__action-btn artdeco-button artdeco-button--2 artdeco-button--secondary ember-view']")
                        for single_btn in get_accept_btns:
                            single_btn.click()
                            print(single_btn)
                            total_accepted_invitation +=1
                            print("Accepted invitations ===>", total_accepted_invitation)
                    print("Finally total invitations accepted ===>", total_accepted_invitation)

                else:
                    print("You have no invitations")

            except ElementNotVisibleException as e:
                print(e)

        except TimeoutException:
            print("Opps Timeout !!!")



    def search_by_filters(self):
        try:
            self.load_credentials()
            current_page = self.current_page
            last_page = self.last_page
            request_count = 0
            url = driver.current_url
            url_end = "&page=" 
            for page in range(0 , last_page):

                if (current_page == 1 ):
                
                    search_element = WebDriverWait(driver , 10 ).until(
                        EC.presence_of_element_located((By.XPATH , "//div[@class='ember-view']/input[@class='search-global-typeahead__input always-show-placeholder']"))
                    )
                    time.sleep(2)
                    search_element.send_keys(self.search_quarry)
                    time.sleep(2)
                    search_element.send_keys(Keys.ENTER)
                    time.sleep(2)
                    url = driver.current_url
                    self.page_scroll()
                    current_page +=1
                
                    user_list = driver.find_elements_by_xpath("//div[@class='blended-srp-results-js pt0 pb4 ph0 container-with-shadow artdeco-card']/ul/li[@class='search-result search-result__occluded-item ember-view']")
                    for user_data in user_list:
                        user_data = user_data.find_elements_by_xpath(".//div/div/div[@class='search-result__info pt3 pb4 ph0']/a/h3/span/span/span[@class='name actor-name']") 
                        for single_user in  user_data: 
                            print("Requesting user to ====>",single_user.text)
                            request_count +=1 
                            print("Total count ====>" , request_count, "\n")
                
                else:
                    
                    driver.get(url + url_end + str(current_page) )
                    time.sleep(1)
                    current_page +=1
                    self.page_scroll()

                    user_list = driver.find_elements_by_xpath("//div[@class='blended-srp-results-js pt0 pb4 ph0 container-with-shadow artdeco-card']/ul/li[@class='search-result search-result__occluded-item ember-view']")
                    for user_data in user_list:
                        user_data = user_data.find_elements_by_xpath(".//div/div/div[@class='search-result__info pt3 pb4 ph0']/a/h3/span/span/span[@class='name actor-name']") 
                        for single_user in  user_data: 
                            print("Requesting user to ====>",single_user.text)
                            request_count +=1 
                            print("Total count ====>" , request_count , "\n")
                        
            print("Finally total request sent  ====>" , request_count , "\n" )
        
        except TimeoutException as t:
            print(t)
      


                
    def page_scroll(self):
        x = 0 
        y = 0
        total_page_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            y += 100
            script = "window"+"."+"scrollTo"+ "(" + str(x)+ "," + str(y) +")"
            driver.execute_script(script)
            time.sleep(0.5)
            if( y >= total_page_height ):
                break
