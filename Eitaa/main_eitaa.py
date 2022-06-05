import datetime
import os
import traceback
from time import sleep, time
import requests
from selenium.webdriver.firefox.options import Options

from file_types import File_types
from Eitaa import config_questions, load_data_util
from Eitaa import contact, downloader
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec


def main(download_path, default_d_path, date_time_addition=None, state="before login", phone_number=None,
         driver=None, tabs_handles=None, config_arr=None, contacts=None):

    download_path = get_dnld_path(download_path, default_d_path)
    try:
        if phone_number is None:
            if is_connected():
                driver = set_driver(download_path)
                config_arr = set_configuration()
                date_time_addition = str(datetime.datetime.today())
                tabs_handles = set_tabs_handles(driver)

            if state == "before login":
                phone_number = login(driver)
                state = "after login"
                sleep(2)

        if state == "after login":
            contacts = get_contacts(config_arr, driver, tabs_handles, date_time_addition)
            state = "after get contacts"

        if state == "after get contacts":
            channels = []
            chats = []
            groups = []
            channels, chats, groups, phone_number = \
                load_data_util.eitaa_downloader(driver, config_arr, tabs_handles,
                                                phone_number, date_time_addition,
                                                channels, chats, groups)

            load_data_util.save_information(channels, chats, contacts, groups,
                                            phone_number, date_time_addition, config_arr)
            state = "after get all messages"

        if state == "after get all messages":
            driver.close()
            return

    except Exception as e:
        traceback.print_exc()
        ok = "0"
        while not is_connected() or ok != "1":
            print("Please check your connection and press 1 to continue.")
            ok = input(">>>\t")
        main(download_path, default_d_path, date_time_addition, state, phone_number, driver=driver,
             tabs_handles=tabs_handles, config_arr=config_arr, contacts=contacts)


def set_driver(download_path):
    # s = Service(GeckoDriverManager().install())
    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.download.panel.shown", False)
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", File_types.types)
    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.dir", download_path)
    option = Options()
    # option.set_preference("driver.download.useDownloadDir", True)
    # option.set_preference("driver.download.panel.shown", False)
    # option.set_preference("driver.helperApps.neverAsk.saveToDisk", File_types.types)
    # option.set_preference("driver.download.folderList", 2)
    # # option.set_preference("driver.download.dir", media_folders_path)
    option.headless = True
    driver = webdriver.Firefox(firefox_profile=profile, options=option)
    driver.set_page_load_timeout(40)
    url = "https://web.eitaa.com/#/login"
    driver.get(url)
    driver.maximize_window()
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    sleep(2)
    return driver


def get_dnld_path(download_path, default_d_path):
    try:
        if download_path == "C:\\RE_downloader_media":
            os.mkdir(default_d_path)
            download_path = download_path + "\\"
        else:
            if download_path[-1] == "\\":
                try:
                    os.mkdir(download_path + "RE_downloader_media")
                    download_path = download_path + "RE_downloader_media\\"
                except (FileExistsError, FileNotFoundError):
                    os.mkdir(default_d_path)
            else:
                try:
                    os.mkdir(download_path + "\\RE_downloader_media")
                    download_path = download_path + "\\RE_downloader_media\\"
                except (FileExistsError, FileNotFoundError):
                    os.mkdir(default_d_path)
                    download_path = download_path + "\\"
    except (FileExistsError, FileNotFoundError):
        pass
    return download_path


def set_configuration():
    config_arr = []
    while True:
        pre_configs = config_questions.use_previous_config()
        configs_title = ["Download photos:", "ِDownload videos?",
                         "Download files", "Download voices",
                         "maximum limit of files(MB):",
                         "Total number of posts from channels:",
                         "Total number of profile pictures:",
                         "capture messages since(hijri)",
                         "Save group members info",
                         "Save group members info",
                         "Export as exel file"]
        index = 0
        print("Current Setting:")
        for title in configs_title:
            print(title + ": " + str(pre_configs[index]))
            index = index + 1

        print("Use current setting?\n1.Yes\n2.NO\n")
        a = input(">>>\t")
        if a == "2":
            config_arr = config_questions.new_config()
            break
        elif a == "1":
            config_arr = config_questions.use_previous_config()
            break
        else:
            print("This is an unaccepted response, enter a valid value")
            continue
    return config_arr


def is_connected():
    url = "https://www.google.com"
    timeout = 10.
    try:
        requests.get(url, timeout=timeout)
        return True
    except (requests.ConnectionError, requests.Timeout):
        return False


# TODO
def get_contacts(config_arr, driver, tabs_handles, date_time_addition):
    contacts = []
    try:
        contacts = contact.get_contacts_info(driver, config_arr, tabs_handles, date_time_addition)
    except ElementNotInteractableException:
        driver.refresh()
        sleep(5)
        contacts = contact.get_contacts_info(driver, config_arr, tabs_handles, date_time_addition)
    return contacts


def set_tabs_handles(driver):
    tabs_handles = None
    try:
        tabs_handles = downloader.open_download(driver)
    except ElementNotInteractableException:
        driver.refresh()
        sleep(5)
        tabs_handles = downloader.open_download(driver)
    return tabs_handles


def login(driver):
    phone_number = get_check_send_phone_number(driver)
    sleep(1)
    ok_button_xpath = "/html/body/div[4]/div[2]/div/div/div[2]/button[2]/span"
    driver.find_element(By.XPATH, ok_button_xpath).click()
    sleep(2)
    phone_number = get_check_send_code(driver, phone_number)
    sleep(1)
    return phone_number


def get_check_send_phone_number(driver):
    while True:
        while True:
            print("Phone Number (Like 9121234567)")
            phone_number = input(">>>\t")
            if len(phone_number) != 10:
                print("Phone number must have 10 digits.")
            elif len(phone_number) == 10:
                break

        phone_number_field_xpath = "/html/body/div[1]/div/div[2]/div[2]/form/div[2]/div[2]/input"
        driver.find_element(By.XPATH, phone_number_field_xpath).send_keys(phone_number)
        sleep(2)

        print("Entered Phone Number:\t"+phone_number)
        print("If it is incorrect, Enter 1; or press any other keys to continue.")
        entry = input(">>>\t")
        if entry == '1':
            driver.refresh()
            continue
        else:
            break

    next_button_xpath = "/html/body/div[1]/div/div[2]/div[1]/div/a/my-i18n"
    driver.find_element(By.XPATH, next_button_xpath).click()
    sleep(3)
    return phone_number


def get_check_send_code(driver, phone_number):
    code_field_xpath = "/html/body/div[1]/div/div[2]/div[2]/form/div[4]/input"
    while ec.url_changes({"https://web.eitaa.com/#/login"}):
        start_time = time()
        while time() < start_time + 70:
            print("SMS Code")
            code = input(">>>\t")
            if len(code) == 5:
                driver.find_element(By.XPATH, code_field_xpath).send_keys(code)
                sleep(3)
                break
            elif ec.visibility_of(driver.find_element(By.XPATH, "/html/body/div[1]/div[1]/div/div/div[1]")):
                break
            else:
                print("Code must have 5 digits.")
        try:
            driver.find_element(By.XPATH, "/html/body/div[1]/div/div[2]/div[2]/form/div[1]/a").click()
            driver.refresh()
            phone_number = login(driver)
            break
        except NoSuchElementException:
            break
    return phone_number


# if __name__ == '__main__':
#     main(download_path, default_d_path)
