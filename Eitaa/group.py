import datetime
from time import sleep
from selenium.common.exceptions import NoSuchElementException
import pandas
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from Eitaa import person


class Group:
    def __init__(self, id, name, members_num, members, photo="", link="", date_time_addition=""):
        self.ID = id
        self.name = name
        self.pro_pic = photo
        self.link = link
        self.members_num = members_num
        self.members = members
        self.date_time_addition = date_time_addition

    def get_title(self):
        return self.name

    def get_info_dict(self):
        data = {
            "name": self.name,
            "photo": self.pro_pic,
            "link": self.link,
            "members#": self.members_num
        }
        return data


def get_group_info(driver, photos, tabs_handles, config_arr, rand_num, date_time_addition):
    wait = WebDriverWait(driver, 40)
    try:
        name = driver.find_element(By.CSS_SELECTOR, "div[class = 'peer_modal_profile_name']").text
    except NoSuchElementException:
        name = ""
    link = get_link(driver, wait)
    members_num = get_members_num(driver)
    members = None
    id = str(hash(str(datetime.datetime.today()) + str(rand_num) + name))
    if config_arr[8] == 1:
        members = get_members(driver, wait, tabs_handles, config_arr, date_time_addition, id)

    return Group(id, name, members_num, members, photos, link, date_time_addition)


# todo: close
def get_link(driver, wait):
    link = ""
    try:
        wait.until(ec.element_to_be_clickable(
            driver.find_element(By.XPATH, "/html/body/div[5]/div[2]/div/div/div[3]/div[1]/div[2]/div/a"))).click()
        sleep(2)
        try:
            try:
                link = driver.find_element(By.XPATH, "/html/body/div[6]/div[2]/div/div/div[1]/div/div/div/div/textarea") \
                    .get_attribute('value')
            except Exception:
                link = driver.find_element(By.CSS_SELECTOR, "textarea[class = 'md-input ng-pristine ng-valid "
                                                            "ng-isolate-scope "
                                                            " ng-not-empty ng-touched']").get_attribute('value')
        except Exception:
            pass
        try:
            wait.until(ec.element_to_be_clickable(
                driver.find_element(By.XPATH, "/html/body/div[6]/div[2]/div/div/div[2]/div/button[1]"))).click()
        except Exception:
            button = driver.find_element(By.CSS_SELECTOR, "button[class = 'btn btn-md']")
            driver.execute_script("arguments[0].click();", button)
    except Exception:
        pass
    return link


def get_members_num(driver):
    try:
        members_num = 0
        members_num_element = driver.find_element(By.XPATH, "/html/body/div[5]/div[2]/div/div/"
                                                            "div[1]/div[2]/div[2]/div[2]").text
        # members_num_element = driver.find_element(By.CSS_SELECTOR,
        #                                           "div[class = 'peer_modal_profile_description ng-scope']"). \
        #     find_element(By.TAG_NAME, "ng-pluralize").text
        # print(members_num_element)
        if members_num_element == "بدون عضو":
            members_num = 0

        elif members_num_element == "یک عضو":
            members_num = 1

        else:
            try:
                members_num = int(members_num[4:])
            except Exception:
                return None
    except Exception:
        members_num = 0

    return members_num


def get_members(driver, wait, tabs_handles, config_arr, date_time_addition, id):
    members = []
    members_element = driver.find_element(By.CSS_SELECTOR, "div[class = 'md_modal_section_peers_wrap']") \
        .find_elements(By.CSS_SELECTOR, "div[class = 'md_modal_list_peer_wrap clearfix ng-scope']")
    members_element = members_element[-config_arr[9]:]
    sleep(1)
    for member in members_element:
        sleep(2)
        try:
            button = member.find_element(By.CSS_SELECTOR, "a[class = "
                                                          "'md_modal_list_peer_photo pull-left"
                                                          " peer_photo_init']")
            driver.execute_script("arguments[0].click();", button)
            sleep(2)
        except Exception:
            wait.until(ec.element_to_be_clickable(
                member.find_element(By.CSS_SELECTOR,
                                    "a[class = 'md_modal_list_peer_name']"))).click()
        sleep(3)
        name, username, phone, profiles, bio = person.get_person_info(driver, config_arr, tabs_handles)
        p = person.Person(phone, profiles, name, username, bio,
                          date_time_addition, "group_member", id)
        # print("member:")
        # print(p.get_info_dict())
        members.append(p)
        sleep(1)

        try:
            try:
                wait.until(ec.element_to_be_clickable(driver.find_element(
                    By.CSS_SELECTOR, "div[class = 'modal-content modal-content-animated']")
                                                      .find_element(By.CSS_SELECTOR,
                                                                    "a[class = 'md_modal_action md_modal_action_close']"))).click()
                try:
                    wait.until(ec.element_to_be_clickable(driver.find_element(
                        By.CSS_SELECTOR, "div[class = 'modal_close_wrap']"))).click()
                except Exception:
                    wait.until(ec.element_to_be_clickable(driver.find_element(
                        By.XPATH, "/html/body/div[5]/div[1]"))).click()
            except Exception:
                wait.until(ec.element_to_be_clickable(driver.find_element(
                    By.XPATH, "/html/body/div[7]/div[2]/div/div/div[1]/div[1]/div[1]/a[1]"))).click()
        except Exception:
            close = driver.find_element(By.XPATH, "/html/body/div[6]")
            driver.execute_script("arguments[0].scrollIntoView();", close)
            action = ActionChains(driver)
            action.move_to_element_with_offset(close, 20, 20)
            action.click()
            action.perform()

        sleep(3)

    return members


def create_groups_df(list_of_groups, account):
    groups_dict = {"name": [], "pro_picture_name": [], "link": [], "num_of_members": [],
                   "conv_id": [], "account": [], "app": [], "date_time_addition": []}
    for group in list_of_groups:
        groups_dict["account"].append(account)
        groups_dict["app"].append('e')
        groups_dict["name"].append(group.name)
        groups_dict["num_of_members"].append(group.members_num)
        # groups_dict["members"].append(group.members)
        groups_dict["link"].append(group.link)
        groups_dict["pro_picture_name"].append(group.pro_pic)
        groups_dict["conv_id"].append(group.ID)
        groups_dict["date_time_addition"].append(group.date_time_addition)
    # print(groups_dict)
    current_conversation_msgs_df = pandas.DataFrame.from_dict(groups_dict)
    groups_df = pandas.DataFrame.head(current_conversation_msgs_df)
    return groups_df


def build_members_list(list_of_groups):
    members = []
    for group in list_of_groups:
        members.append(group.members)
    return members
