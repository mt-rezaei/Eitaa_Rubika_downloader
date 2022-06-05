import pandas
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from Eitaa import downloader


class Person:
    def __init__(self, phone="NULL", profiles="NULL", name="NULL", username="NULL",
                 bio="NULL", date_time_addition="", person_type="contact", group_id="NULL"):
        self.phone = phone
        self.pro_pic = profiles
        self.name = name
        self.id = username
        self.bio = bio
        self.date_time_addition = date_time_addition
        self.person_type = person_type
        self.group_id = group_id

    def get_name(self):
        return self.name

    # def get_info_dict(self):
    #     data = {
    #         "phone": self.phone,
    #         "profiles": self.pro_pic,
    #         "name": self.name,
    #         "username": self.id,
    #         "bio": self.bio
    #     }
    #     return data


def get_person_info(driver, config_arr, tabs_handles):
    # TODO
    # profiles = downloader.get_profile_photos(driver, config_arr, tabs_handles)
    profiles = "NULL"
    try:
        try:
            name = driver.find_element(By.XPATH, "/html/body/div[5]/div[2]/div/div/div[1]/div[2]/div[2]/div[1]").text
        except NoSuchElementException:
            name = driver.find_element(By.CSS_SELECTOR, "div[class = 'peer_modal_profile_name']").text
    except NoSuchElementException:
        # print("can not found profile name")
        name = "NULL"

    arr = driver.find_elements(By.CSS_SELECTOR, "div[class = 'md_modal_section_param_wrap ng-scope']")
    phone = "NULL"
    username = "NULL"
    bio = "NULL"
    for item in arr:
        if item.get_attribute("ng-if") == "user.phone":
            phone = item.find_element(By.CSS_SELECTOR, "div[class = 'md_modal_section_param_value ng-binding']").text
        elif item.get_attribute("ng-if") == "user.username":
            username = item.find_element(By.CSS_SELECTOR, "span[class = 'ng-binding']").text
        elif item.get_attribute("ng-if") == "rAbout":
            bio = item.find_element(By.CSS_SELECTOR, "span[class = 'ng-binding']").text

    return name, username, phone, profiles, bio


def create_persons_dict(list_of_persons1, list_of_persons2, account):
    list_of_persons = list_of_persons1 + list_of_persons2
    persons_dict = {"name": [], "phone": [], "id": [], "biography": [], "pro_picture_name": [],
                    "account": [], "app": [], "date_time_addition": [], "person_type": [], "conv_id": []}
    for inner_list in list_of_persons:
        for person in inner_list:
            persons_dict["account"].append(account)
            persons_dict["app"].append('E')
            persons_dict["name"].append(person.name)
            persons_dict["phone"].append(person.phone)
            persons_dict["id"].append(person.id)
            persons_dict["biography"].append(person.bio)
            persons_dict["pro_picture_name"].append(person.pro_pic)
            persons_dict["date_time_addition"].append(person.date_time_addition)
            persons_dict["person_type"].append(person.person_type)
            persons_dict["conv_id"].append(person.group_id)
        return persons_dict


def create_persons_df(list_of_persons1, list_of_persons2, account):
    persons_dict = create_persons_dict(list_of_persons1, list_of_persons2, account)
    # print(persons_dict)
    persons_df = pandas.DataFrame.from_dict(persons_dict)
    return persons_df
