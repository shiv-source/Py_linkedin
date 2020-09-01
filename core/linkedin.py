from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import ElementNotVisibleException, TimeoutException
from selenium.webdriver.chrome.options import Options
import time
from core.utils.cookies import load_cookie,save_cookie
from core.utils.loader import get_path
import pickle


options = Options()
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(executable_path=get_path("driver" , "chromedriver.exe"), options= options)
driver.maximize_window()
driver.implicitly_wait(10)


driver.get("https://www.linkedin.com/")
load_cookie(driver, get_path("cookies" , "cookies.txt"))
driver.refresh()


class Linkedin(object):

    def __init__(self , username , password, login_url):

        self.username = username
        self.password = password
        self.login_url = login_url


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
        try:
            driver.get("https://www.linkedin.com/mynetwork/")
            try:
                time.sleep(5)

                """
                Collepsing the pop up chat message box
                """
                msg_popup = driver.find_elements_by_xpath("//*[@id='msg-overlay']/div[1]/header")
                for popup in msg_popup:
                    popup.click()
                
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





