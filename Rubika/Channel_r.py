import pandas
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
# , ElementNotInteractableException
from Rubika.Downloaders_r import Downloaders


class Channel:

    def __init__(self):
        self.name = ""
        self.link = ""
        self.pro_pic_name = ""
        self.members_num = ""
        self.bio = ""
        self.conv_id = ""
        self.date_time_addition = ""

    def get_channel_info(self, browser, tabs_handles, profile_num):
        self.name = self.get_name(browser)
        self.bio = self.get_bio(browser)
        self.pro_pic_name = Downloaders.download_pro_pic(browser, tabs_handles, profile_num)
        # self.link = self.get_link(browser)
        self.members_num = self.get_mems_num(browser)
        # try:
        #     browser.find_element(By.XPATH, "/html/body/app-root/div/div/div[3]/sidebar-container/div/sidebar-view/"
        #                                    "div/modal-channel-info/div[1]/button").click()
        # except ElementNotInteractableException:
        #     browser.back()

    @staticmethod
    def get_name(browser):
        name = browser.find_element(By.CSS_SELECTOR, "div[class = 'profile-avatars-info']"). \
            find_element(By.CSS_SELECTOR, "div[class = 'profile-name']"). \
            find_element(By.CSS_SELECTOR, "span[class = 'peer-title']").text
        if name != "":
            return name
        else:
            return "NULL"

    @staticmethod
    def get_link(browser):
        try:
            link = browser.find_element(By.CSS_SELECTOR,
                                        "div[class = 'md_modal_iconed_section_wrap md_modal_iconed_section_number']").\
                find_element(By.CSS_SELECTOR, "a[class = 'settings_modal_username_link']").text
            return link
        except NoSuchElementException:
            return "NULL"

    @staticmethod
    def get_bio(browser):
        try:
            bio = browser.find_element(By.CSS_SELECTOR,
                                       "div[class = 'sidebar-left-section-content']").\
                find_element(By.CSS_SELECTOR, "div[class = 'row row-with-icon row-with-padding row-clickable"
                                              " hover-effect rp']").\
                find_element(By.CSS_SELECTOR, "div[class = 'row-title rbico rbico-username']").text
            return bio
        except NoSuchElementException:
            return "NULL"

    @staticmethod
    def get_mems_num(browser):
        try:
            mems_num = browser.find_element(By.CSS_SELECTOR, "div[class = 'profile-avatars-container is-single']").\
                find_element(By.CSS_SELECTOR, "div[class = 'profile-avatars-info']").\
                find_element(By.CSS_SELECTOR, "div[class = 'profile-subtitle']").\
                find_element(By.TAG_NAME, "span").text
            # mems_num = mems_num.split(" ")
            if mems_num is not None:
                mems_num = mems_num.split(" ")
                return mems_num[0]
            else:
                return "NULL"
        except NoSuchElementException:
            return "NULL"

    def set_channel_id(self, conv_id, date_time_addition):
        self.conv_id = conv_id
        self.date_time_addition = date_time_addition

    @staticmethod
    def create_channels_dict(list_of_channels, account):
        channels_dict = {"name": [], "pro_picture_name": [], "link": [], "num_of_members": [], "about": [],
                         "conv_id": [], "account": [], "app": [], "date_time_addition": []}
        for channel in list_of_channels:
            channels_dict["account"].append(account)
            channels_dict["app"].append('R')
            channels_dict["name"].append(channel.name)
            channels_dict["num_of_members"].append(channel.members_num)
            channels_dict["about"].append(channel.bio)
            channels_dict["link"].append(channel.link)
            channels_dict["pro_picture_name"].append(str(channel.pro_pic_name))
            channels_dict["conv_id"].append(channel.conv_id)
            channels_dict["date_time_addition"].append(channel.date_time_addition)
        return channels_dict

    @staticmethod
    def create_channels_df(list_of_channels, account):
        channels_dict = Channel.create_channels_dict(list_of_channels, account)
        # print(channels_dict)
        channels_df = pandas.DataFrame.from_dict(channels_dict)
        return channels_df
