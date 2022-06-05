from time import sleep
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from Eitaa import person


def open_contacts_list(driver, wait):
    try:
        wait.until(ec.element_to_be_clickable(driver.find_element(By.CSS_SELECTOR, "a[class = 'tg_head_btn "
                                                                                   "dropdown-toggle']"))).click()
        sleep(1)
        e = driver.find_element(By.CSS_SELECTOR, "ul[class = 'dropdown-menu']"). \
            find_element(By.CSS_SELECTOR, "li[class = 'ng-scope']")
        wait.until(ec.element_to_be_clickable(e.find_element(By.TAG_NAME, 'a'))).click()
        sleep(2)
        e1 = driver.find_element(By.CSS_SELECTOR, "div[class = 'contacts_modal_wrap md_modal_wrap ng-scope']"). \
            find_element(By.CSS_SELECTOR,
                         "ul[class = 'contacts_modal_members_list nav nav-pills nav-stacked ng-scope']")
        contacts = e1.find_elements(By.TAG_NAME, 'li')
    except Exception:
        contacts = None
    return contacts


def get_contacts_info(driver, config_arr, tabs_handles, date_time_addition):
    wait = WebDriverWait(driver, 10)
    contacts = open_contacts_list(driver, wait)

    contacts_info = []
    if contacts is not None:
        for i in range(len(contacts)):

            try:
                e2 = contacts[i].find_element(By.CSS_SELECTOR, "a[class = 'contacts_modal_contact']")
                wait.until(ec.element_to_be_clickable(e2)).click()
                sleep(2)
                e3 = driver.find_element(By.CSS_SELECTOR, "div[class = 'tg_head_main_wrap']"). \
                    find_element(By.CSS_SELECTOR, "a[class = 'tg_head_btn ng-scope']")
                driver.execute_script("arguments[0].scrollIntoView();", e3)
                wait.until(ec.element_to_be_clickable(e3)).click()
                sleep(2)
            except (NoSuchElementException, TimeoutException):
                print("can not find contact information")

            name, username, phone, profiles, bio = person.get_person_info(driver, config_arr, tabs_handles)

            info = person.Person(phone, profiles, name, username, bio, date_time_addition)
            contacts_info.append(info)

            wait.until(ec.element_to_be_clickable(driver.find_element(By.CSS_SELECTOR,
                                                                      "div[class = 'modal_close_wrap']"))).click()
            sleep(1)
            i += 1
            if i < len(contacts):
                contacts = open_contacts_list(driver, wait)

    try:
        wait.until(ec.element_to_be_clickable(driver.find_element(
            By.XPATH, "/html/body/div[5]/div[2]/div/div/div[1]/div[1]/div/a[1]"))).click()
    except Exception:
        pass

    return contacts_info
