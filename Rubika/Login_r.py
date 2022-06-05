import traceback

from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.support import expected_conditions as EC
import requests
import time
from file_types import File_types


class Login:
    @staticmethod
    def set_browser(media_folder_path, login_page_url):
        option = Options()
        option.set_preference("browser.download.useDownloadDir", True)
        option.set_preference("browser.download.panel.shown", False)
        option.set_preference("browser.helperApps.neverAsk.saveToDisk", File_types.types)
        # option.set_preference("browser.helperApps.neverAsk.openFile", 'application/pdf, application/x-pdf')
        option.set_preference("browser.download.folderList", 2)
        option.set_preference("browser.download.dir", media_folder_path)
        option.headless = True
        # Add proxy
        # option.add_argument('proxy-server=106.122.8.54:3128')
        browser = webdriver.Firefox(options=option)
        browser.set_page_load_timeout(20)
        browser.get(login_page_url)
        browser.maximize_window()
        # Remove navigator.webdriver Flag using JavaScript
        browser.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        return browser

    @classmethod
    def send_phone_num(cls, browser, phone_number_field_selector='', next_button_selector='',
                       yes_button_selector=''):
        phone_num = ''
        # enter phone number
        while True:
            while True:
                print("Phone Number (Like 9121234567)")
                phone_num = input(">>>\t")
                if len(phone_num) != 10:
                    print("Phone number should have 10 digits.")
                elif len(phone_num) == 10:
                    break
            print("Entered Phone Number:\t" + phone_num)
            print("If it is incorrect, Enter 1; or press any other keys to continue.")
            entry = input(">>>\t")
            if entry == '1':
                # browser.refresh()
                continue
            else:
                break
        try:
            if not EC.url_matches("https://web.rubika.ir/#/login/"):
                return phone_num
            phone_num_field_is_loaded = EC.visibility_of(browser.find_element(By.XPATH, phone_number_field_selector))
            if phone_num_field_is_loaded:
                browser.find_element(By.XPATH, phone_number_field_selector).clear()
                browser.find_element(By.XPATH, phone_number_field_selector).send_keys(phone_num)
            else:
                while not phone_num_field_is_loaded:
                    browser.refresh()
                    sleep(3)
                browser.find_element(By.XPATH, phone_number_field_selector).clear()
                browser.find_element(By.XPATH, phone_number_field_selector).send_keys(phone_num)
        except NoSuchElementException:
            # traceback.print_exc()
            if EC.url_matches("https://web.rubika.ir/"):
                return phone_num
            else:
                print("Error occurred while signing in! Please try again!")
                browser.refresh()
                cls.send_phone_num(browser, phone_number_field_selector, next_button_selector,
                                   yes_button_selector)
        # click on next button
        try:
            sleep(2)
            browser.find_element(By.XPATH, next_button_selector).click()
        except NoSuchElementException:
            try:
                cls.send_phone_num(browser, phone_number_field_selector, next_button_selector, yes_button_selector)
            except:
                pass
        return phone_num

    @classmethod
    def send_code(cls, browser, code_field_xpath, login_page_url, phone_number_field_selector, next_button_xpath,
                  yes_button_xpath):
        code = None
        while EC.url_matches(login_page_url):
            if code is None:
                start_time = time.time()
                while time.time() < start_time + 200:
                    print("sms code:")
                    print("(If it take so long and you didn't receive code,please enter 123456 to continue.)")
                    code = input(">>>\t")
                    if len(code) != 6:
                        print("Phone number must have 6 digits.")
                    elif len(code) == 6:
                        break
                try:
                    browser.find_element(By.XPATH, code_field_xpath).send_keys(code)
                    sleep(3)
                    try:
                        browser.find_element(By.CSS_SELECTOR, "div[class = 'phone-wrapper']") \
                            .find_element(By.CSS_SELECTOR, "span[class = 'phone-edit rbico-edit']").click()
                        cls.login(browser, phone_number_field_selector, next_button_xpath, yes_button_xpath)
                        cls.send_code(browser, code_field_xpath, phone_number_field_selector, login_page_url,
                                      next_button_xpath, yes_button_xpath)
                        break
                    except:
                        sleep(3)
                        break
                except NoSuchElementException:
                    # print(3)
                    browser.refresh()
                    if not browser.find_elements(By.CSS_SELECTOR, "div[class = 'im_dialogs_col_wrap noselect']"):
                        cls.login(browser, phone_number_field_selector, next_button_xpath, yes_button_xpath)
                        cls.send_code(browser, code_field_xpath, phone_number_field_selector, login_page_url,
                                      next_button_xpath, yes_button_xpath)
                    # print("An error occurred while signing in! Please try again.")
                    break

    @staticmethod
    def is_connected():
        url = "https://www.google.com"
        timeout = 5
        try:
            requests.get(url, timeout=timeout)
            return True
        except (requests.ConnectionError, requests.Timeout):
            return False

    @classmethod
    def login(cls, browser, phone_number_field_selector='', next_button_selector='', yes_button_selector=''):
        phone_num = ''
        try:
            phone_num = cls.send_phone_num(browser, phone_number_field_selector, next_button_selector,
                                           yes_button_selector)
        except NoSuchElementException:
            # traceback.print_exc()
            while True:
                # try to find "کد را وارد کنید":
                try:
                    browser.find_element(By.XPATH,
                                         "/html/body/app-root/tab-login/div/div/div[2]/div[2]/div/p/span")
                    # if we are in code page --> break
                    break
                # if we are in first page:
                except NoSuchElementException:
                    phone_num = cls.send_phone_num(browser, phone_number_field_selector, next_button_selector,
                                                   yes_button_selector)
        return phone_num
