import pandas
from Rubika.Downloaders_r import Downloaders
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException


class Person:
    def __init__(self):
        self.name = "NULL"
        self.phone = "NULL"
        self.id = "NULL"
        self.bio = "NULL"
        self.pro_pic = "NULL"
        self.date_time_addition = "NULL"
        self.person_type = "group_member"
        self.group_id = "Null"

    def get_person_info(self, browser, tabs_handles, profile_num):
        try:
            self.name = browser.find_element(By.CSS_SELECTOR, "div[class = 'profile-avatars-container is-single']")\
                .find_element(By.CSS_SELECTOR, "div[class = 'profile-avatars-info']") \
                .find_element(By.CSS_SELECTOR, "div[class = 'profile-name']") \
                .find_element(By.CSS_SELECTOR, "span[class = 'peer-title']").text
            # print("name :)")
        except NoSuchElementException:
            self.name = "NULL"
        try:
            self.phone = browser.find_element(By.CSS_SELECTOR, "div[class = 'row-title rbico rbico-phone']").text
            # print("phone number:)")
        except NoSuchElementException:
            self.phone = "NULL"
        try:
            self.id = browser.find_element(By.CSS_SELECTOR, "div[class = 'row-title rbico rbico-phone']").text
            # print("id :)")
        except NoSuchElementException:
            self.id = "NULL"
        try:
            self.bio = browser.find_element(By.CSS_SELECTOR, "div[class = 'row-title rbico rbico-info pre-wrap']").text
            # print("bio :)")
        except NoSuchElementException:
            self.bio = "NULL"
        self.pro_pic = Downloaders.download_pro_pic(browser, tabs_handles, profile_num)
        try:
            browser.back()
        except (ElementNotInteractableException, NoSuchElementException):
            browser.find_element(By.XPATH, "/html/body/app-root/div/div/div[3]/sidebar-container/div/"
                                           "sidebar-view/div/div/div[1]/button").click()
        return self

    @staticmethod
    def create_persons_dict(list_of_persons, account):
        persons_dict = {"saved_name": [], "phone_number": [], "id": [], "biography": [], "pro_picture_name": [],
                        "account": [], "app": [], "date_time_addition": [], "person_type": [], "conv_id": []}
        for person in list_of_persons:
            persons_dict["account"].append(account)
            persons_dict["app"].append('R')
            persons_dict["saved_name"].append(person.name)
            persons_dict["phone_number"].append(person.phone)
            persons_dict["id"].append(person.id)
            persons_dict["biography"].append(person.bio)
            persons_dict["pro_picture_name"].append(person.pro_pic)
            persons_dict["date_time_addition"].append(person.date_time_addition)
            persons_dict["person_type"].append(person.person_type)
            persons_dict["conv_id"].append(person.group_id)
        return persons_dict

    @staticmethod
    def create_persons_df(list_of_persons, account):
        persons_dict = Person.create_persons_dict(list_of_persons, account)
        # print(persons_dict)
        persons_df = pandas.DataFrame.from_dict(persons_dict)
        pandas.DataFrame.head(persons_df)
        return persons_df
