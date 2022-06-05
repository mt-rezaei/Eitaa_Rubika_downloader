import pandas
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from time import sleep
from Rubika.Person_r import Person


def open_contact_list(browser):
    browser.find_element(By.XPATH, "/html/body/app-root/div/div/div[1]/sidebar-container"
                                   "/div/sidebar-view/div/rb-chats/div[1]/div[1]/div[2]/div/div").click()
    sleep(2)
    contacts_btn = browser.find_element(By.CSS_SELECTOR, "div[class = 'btn-menu bottom-right has-footer active']")\
        .find_element(By.CSS_SELECTOR, "div[class = 'btn-menu-item rbico-user rp']")\
        .find_element(By.CSS_SELECTOR, "div[class = 'c-ripple rp']").click()
    sleep(3)


def get_contacts(browser, profile_num, tabs_handles):
    saved_contacts = []
    open_contact_list(browser)
    try:
        sleep(4)
        print("Capturing contacts info ...")
        contacts = browser.find_element(By.XPATH, "/html/body/app-root/div/div/div[1]/sidebar-container/"
                                                  "div/sidebar-view[1]/div/modal-contacts/div[2]/div/ul")\
            .find_elements(By.TAG_NAME, "li")

        for i in range(len(contacts)):
            contacts = browser.find_element(By.XPATH, "/html/body/app-root/div/div/div[1]/sidebar-container/"
                                                      "div/sidebar-view[1]/div/modal-contacts/div[2]/div/ul") \
                .find_elements(By.TAG_NAME, "li")
            contact = contacts[i]
            contact.click()
            try:
                head = browser.find_element(By.XPATH, "/html/body/app-root/div/div/div[2]/tab-container"
                                                      "/div/tab-view/div/tab-conversation/div[1]/div[1]").click()
            except:
                # print("Can't click on head.(get_contacts)")
                pass
            sleep(2)
            saved_contact = Person()
            saved_contacts.append(saved_contact.get_person_info(browser, tabs_handles, profile_num))
            if i < len(contacts) - 1:
                open_contact_list(browser)
    except NoSuchElementException:
        print("can't find contacts list.")
    return saved_contacts


# def set_contact_id(self, conv_id, date_time_addition):
#     self.conv_id = conv_id
#     self.date_time_addition = date_time_addition


def creat_contact_df(list_of_contacts, account, date_time_addition):
    contacts_info_dict = {"saved_name": [],
                          "phone_number": [],
                          "id": [],
                          "biography": [],
                          "pro_picture_name": [],
                          "account": [],
                          "app": [],
                          "date_time_addition": [],
                          "person_type": [],
                          "group_id": []}
    for contact in list_of_contacts:
        contacts_info_dict["date_time_addition"].append(date_time_addition)
        contacts_info_dict["account"].append(account)
        contacts_info_dict["app"].append('R')
        contacts_info_dict["saved_name"].append(contact.name)
        contacts_info_dict["phone_number"].append(contact.phone)
        contacts_info_dict["id"].append(contact.id)
        contacts_info_dict["biography"].append(contact.bio)
        contacts_info_dict["pro_picture_name"].append(str(contact.pro_pic))
        contacts_info_dict["person_type"].append("contact")
        contacts_info_dict["group_id"].append(contact.group_id)

    contacts_info_df = pandas.DataFrame(contacts_info_dict)
    return contacts_info_df
