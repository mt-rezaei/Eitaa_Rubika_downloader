from time import sleep
import pandas
from selenium.webdriver.common.by import By
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as ec
from Rubika.Downloaders_r import Downloaders
from Rubika.Person_r import Person
from selenium.common.exceptions import NoSuchElementException
# ,  ElementNotInteractableException
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.webdriver.support.wait import WebDriverWait


class Group:

    conv_ul_xpath = "/html/body/div[1]/app-root/span/div[1]/div/rb-chats/div/div[2]/div/div[1]/ul[2]"

    def __init__(self):
        self.name = ""
        self.pro_pic = ""
        self.link = ""
        self.members_num = ""
        self.members = ""
        self.conv_id = ""
        self.date_time_addition = ""

    def get_group_info(self, browser, tabs_handles, profile_num, max_members, conv_num):
        try:
            self.name = browser.find_element(By.XPATH, "/html/body/app-root/div/div/div[2]/tab-container/div/"
                                                       "tab-view/div/tab-conversation/div[1]/div[1]/div/div[2]/div[1]"
                                                       "/div/span").text
        except:
            self.name = "NULL"
        self.link = self.get_link(browser)
        self.members_num = self.get_members_num(browser)
        self.pro_pic = Downloaders.download_pro_pic(browser, tabs_handles, profile_num)
        self.members = self.get_members(browser, tabs_handles, profile_num, max_members, conv_num)
        try:
            browser.find_element(By.CSS_SELECTOR, "button[class = 'btn-icon sidebar-close-button']").click()
        except:
            browser.back()
        return self

    @staticmethod
    def get_link(browser):
        try:
            browser.find_element(By.XPATH, "/html/body/app-root/div/div/div[3]/sidebar-container"
                                           "/div/sidebar-view/div/modal-chat-info/div[1]/div/div[1]"
                                           "/button/div/div").click()
            sleep(2)
            try:
                browser.find_element(By.XPATH, "/html/body/app-root/div/div/div[3]/"
                                               "sidebar-container/div/sidebar-view[1]/div/"
                                               "modal-group-edit/div[2]/div/form/div/div[3]/div[1]/div").click()
                try:
                    link = browser.find_element(By.XPATH, "/html/body/app-root/div/div/div[3]/sidebar-container"
                                                          "/div/sidebar-view[1]/div/modal-group-settings/div[2]/"
                                                          "div/div/div/div/div/label[3]/div[2]/span").text
                    browser.back()
                    browser.back()
                    return link
                except:
                    browser.back()
                    browser.back()
                    return "NULL"
            except:
                browser.back()
                return "NULL"
        except:
            return "NULL"

    @staticmethod
    def get_members_num(browser):
        members_num = "NULL"
        sleep(3)
        try:
            members_num = browser.find_element(By.XPATH, "/html/body/app-root/div/div/div[2]/tab-container/"
                                                         "div/tab-view/div/tab-conversation/div[1]/div[1]/"
                                                         "div/div[2]/div[2]/div/span").text
        except NoSuchElementException:
            pass
            # print("can't get number of group members.")
        members_num = members_num.split(" ")
        try:
            members_num = int(members_num[0])
            # print("Number of members:\t"+str(members_num))
        except ValueError:
            members_num = 0
        return str(members_num)

    @staticmethod
    def get_members(browser, tabs_handles, profile_num, max_members, conv_num):
        members_info = []
        #TODO
        try:
            # browser.execute_script("window.scrollTo(0, 500)")
            members_list = browser.find_element(By.CSS_SELECTOR, "div[class = 'search-super-content-members']")\
                .find_element(By.TAG_NAME, "rb-chat-members")\
                .find_element(By.CSS_SELECTOR, "ul[class = 'chatlist']").find_elements(By.TAG_NAME, "li")
            # print("MEMBER LIST FOUNDED.")
        except NoSuchElementException:
            # print(1)
            sleep(3)
            try:
                members_list = browser.find_elements(By.XPATH, "/html/body/app-root/div/div/div[3]/"
                                                               "sidebar-container/div/sidebar-view/div/"
                                                               "modal-chat-info/div[2]/div/div/rb-chat-media"
                                                               "/div/div[2]/div[1]/div/rb-chat-members/ul")\
                    .find_elements(By.TAG_NAME, "li")
            except:
                return members_info
        try:
            if max_members == "0":
                max_members = len(members_list)
            for i in range(int(max_members)):
                try:
                    members_list = browser.find_element(By.CSS_SELECTOR,
                                                        "div[class = 'search-super-content-members']") \
                        .find_element(By.TAG_NAME, "rb-chat-members") \
                        .find_element(By.CSS_SELECTOR, "ul[class = 'chatlist']").find_elements(By.TAG_NAME, "li")
                except NoSuchElementException:
                    # print(2)
                    members_list = browser.find_elements(By.XPATH, "/html/body/app-root/div/div/div[3]/"
                                                                   "sidebar-container/div/sidebar-view/div/"
                                                                   "modal-chat-info/div[2]/div/div/rb-chat-media"
                                                                   "/div/div[2]/div[1]/div/rb-chat-members/ul") \
                        .find_elements(By.TAG_NAME, "li")
                member = members_list[i]
                browser.execute_script("arguments[0].scrollIntoView();", member)
                member.click()
                sleep(2)
                member_info = Person()
                member_info = member_info.get_person_info(browser, tabs_handles, profile_num)
                members_info.append(member_info)
                conv_list = Group.get_conv_list(browser, Group.conv_ul_xpath)
                conv = conv_list[conv_num]
                try:
                    conv.click()
                except:
                    conv.click()
                sleep(2)
        except NoSuchElementException:
            print("Can't get group members!")
        return members_info

    def set_group_id(self, conv_id, date_time_addition):
        self.conv_id = conv_id
        self.date_time_addition = date_time_addition

    @staticmethod
    def build_members_list(list_of_groups, date_time_addition):
        members = []
        for group in list_of_groups:
            for member in group.members:
                member.group_id = group.conv_id
                member.person_type = "group_member"
                member.date_time_addition = date_time_addition
            members = members + group.members
        return members

    @staticmethod
    def create_groups_df(list_of_groups, account):
        groups_dict = {"name": [], "pro_picture_name": [], "link": [], "num_of_members": [],
                       "conv_id": [], "account": [], "app": [], "date_time_addition": []}
        for group in list_of_groups:
            groups_dict["account"].append(account)
            groups_dict["app"].append('R')
            groups_dict["name"].append(group.name)
            groups_dict["num_of_members"].append(group.members_num)
            # groups_dict["members"].append(group.members)
            groups_dict["link"].append(group.link)
            groups_dict["pro_picture_name"].append(str(group.pro_pic))
            groups_dict["conv_id"].append(group.conv_id)
            groups_dict["date_time_addition"].append(group.date_time_addition)
        groups_df = pandas.DataFrame.from_dict(groups_dict)
        return groups_df

    @staticmethod
    def get_conv_list(browser, conv_list_xpath):
        convs_ul_tags = browser.find_element(By.CSS_SELECTOR,
                                             "div[class = 'scrollable scrollable-y sidebar-slider-item active']") \
            .find_elements(By.TAG_NAME, "ul")
        if len(convs_ul_tags) == 2:
            conv_list = convs_ul_tags[1].find_elements(By.TAG_NAME, 'li')
        else:
            conv_list = convs_ul_tags[0].find_elements(By.TAG_NAME, 'li')
        return conv_list
