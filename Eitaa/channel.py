import datetime
from selenium.common.exceptions import NoSuchElementException
import pandas
from selenium.webdriver.common.by import By
from Eitaa import group


class Channel:
    def __init__(self, id, name, photo, link, bio, members_num, date_time_addition):
        self.name = name
        self.pro_pic = photo
        self.link = link
        self.bio = bio
        self.members_num = members_num
        self.id = id
        self.date_time_addition = date_time_addition

    # def set_messages(self, messages):
    #     self.messages = messages

    def get_title(self):
        return self.name

    # def get_messages(self):
    #     return self.messages

    def get_info_dict(self):
        data = {
            "name": self.name,
            "photo": self.pro_pic,
            "link": self.link,
            "bio": self.bio,
            "members#": self.members_num
        }
        return data

    def to_string(self):
        return "name: " + self.name + "bio: " + self.bio + "members num: " + self.members_num \
               + "photo: " + self.pro_pic + "link: " + self.link


def get_channel_info(driver, photos, rand_num, date_time_addition):
    try:
        name = driver.find_element(By.CSS_SELECTOR, "div[class = 'peer_modal_profile_name']").text
    except NoSuchElementException:
        name = ""
    link = get_link(driver)
    members_num = group.get_members_num(driver)
    bio = get_bio(driver)
    id = str(hash(str(datetime.datetime.today()) + str(rand_num) + name))
    return Channel(id, name, photos, link, bio, members_num, date_time_addition)


def get_link(driver):
    try:
        return driver.find_element(By.CSS_SELECTOR,
                                   "a[class = 'settings_modal_username_link ng-binding']").text
    except NoSuchElementException:
        return ""


def get_bio(driver):
    try:
        arr = driver.find_elements(By.CSS_SELECTOR, "div[class = 'md_modal_section_param_wrap ng-scope']")
        for item in arr:
            value = item.find_element(By.CSS_SELECTOR, "div[class = 'md_modal_section_param_value']")
            name = item.find_element(By.CSS_SELECTOR, "div[class = 'md_modal_section_param_name']")
            if name.get_attribute("my-i18n") == "توضیحات":
                return value.find_element(By.CSS_SELECTOR, "span[class = 'ng-binding']").text
        return ""
    except Exception:
        return ""


def get_channels_dict(channels_list, account):
    channels_dict = {"name": [], "pro_pictures_name": [], "link": [], "num_of_members": [], "about": [],
                     "conv_id": [], "account": [], "app": [], "date_time_addition": []}
    for channel in channels_list:
        channels_dict["account"].append(account)
        channels_dict["app"].append('E')
        channels_dict["name"].append(channel.name)
        channels_dict["num_of_members"].append(channel.members_num)
        channels_dict["about"].append(channel.bio)
        channels_dict["link"].append(channel.link)
        channels_dict["pro_pictures_name"].append(channel.pro_pic)
        channels_dict["conv_id"].append(channel.id)
        channels_dict["date_time_addition"].append(channel.date_time_addition)
    return channels_dict


def create_channels_df(channels_list, account):
    channels_dict = get_channels_dict(channels_list, account)
    # print(channels_dict)
    channels_df = pandas.DataFrame.from_dict(channels_dict)
    return channels_df
