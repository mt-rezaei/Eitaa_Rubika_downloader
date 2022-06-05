import datetime
import os
import random
import traceback
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
# ElementNotInteractableException
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.support import expected_conditions as EC
from DB import DB
from Rubika import Contacts_r
from Rubika.Login_r import Login
from Rubika.Message_r import Message
import pandas
from Rubika.Configs_r import Configs
from Rubika.Downloaders_r import Downloaders
from Rubika.Channel_r import Channel
from Rubika.Group_r import Group
from Rubika.Chat_r import Chat
import socket
from Rubika.Person_r import Person


def scroll_up_messages(firefox_browser):
    try:
        try:
            handle = firefox_browser.find_element(By.CSS_SELECTOR, "div[class='bubbles-date-group']")\
                .find_element(By.CSS_SELECTOR, "span[class = 'time rbico']")
            handle.click()
        except:
            msgs = firefox_browser.find_elements(By.CSS_SELECTOR, "div[class='bubbles-date-group']")
            first_msg = msgs[0]
            browser.execute_script("arguments[0].scrollIntoView();", first_msg)
        scrollable_element = firefox_browser.find_element(By.CSS_SELECTOR,
                                                          "div[class = 'scrollable scrollable-y']")
        firefox_browser.execute_script('return arguments[0].scrollBy(0, -50)', scrollable_element)
    except:
        firefox_browser.execute_script("window.scrollTo(0, 500)")


def fetch_conv_messages(conv_element, browser, c_type, msg_num):
    sleep(2)
    current_messages = browser.find_elements(By.CSS_SELECTOR, "div[class = 'bubbles-date-group']")
    all_messages_are_loaded = False
    counter = 0
    while not all_messages_are_loaded:
        scroll_up_messages(browser)
        previous_messages = current_messages
        current_messages = browser.find_elements(By.CSS_SELECTOR, "div[class = 'bubbles-date-group']")
        if current_messages == previous_messages and counter >= 3:
            all_messages_are_loaded = True
        elif c_type == "channel" and len(current_messages) > int(float(msg_num)):
            current_messages = current_messages[-msg_num:]
            all_messages_are_loaded = True
        else:
            sleep(3)
            counter = counter + 1
            scroll_up_messages(browser)
            if current_messages == previous_messages:
                all_messages_are_loaded = True

    scroll_up_messages(browser)
    try:
        conv_messages = browser.find_elements(By.CSS_SELECTOR, "div[class = 'bubbles-date-group']")
    except NoSuchElementException:
        conv_messages = browser.find_elements(By.CSS_SELECTOR, "div[class = 'bubbles-date-group']")
        # "bubbles-inner has-rights is-chat"
        # "bubbles-inner is-channel"
        # "bubbles-inner"
    try:
        browser.find_element(By.CSS_SELECTOR, "a[class = 'btn btn-md btn-md-primary im_edit_cancel_link']").click()
        return conv_messages
    except NoSuchElementException:
        return conv_messages


def get_conv_list(browser, conv_list_xpath):
    convs_ul_tags = browser.find_element(By.CSS_SELECTOR,
                                         "div[class = 'scrollable scrollable-y sidebar-slider-item active']")\
        .find_elements(By.TAG_NAME, "ul")
    if len(convs_ul_tags) == 2:
        conv_list = convs_ul_tags[1].find_elements(By.TAG_NAME, 'li')
    else:
        conv_list = convs_ul_tags[0].find_elements(By.TAG_NAME, 'li')
    return conv_list


def conv_type(browser):
    sleep(2)
    try:
        browser.find_element(By.CSS_SELECTOR, "div[class = 'chat-info']")\
            .find_element(By.CSS_SELECTOR, "div[class = 'person']").click()
        sleep(3)
    except:
        pass
    title = ''
    try:
        title = browser.find_element(By.CLASS_NAME, "page-component")\
            .find_element(By.CSS_SELECTOR, "div[class = 'sidebar-header']")\
            .find_element(By.CSS_SELECTOR, "div[class = 'sidebar-header__title']").text
        # print("TITLE FOUNDED!")
    except:
        try:
            title = browser.find_element(By.XPATH, "/html/body/app-root/div/div/div[3]/sidebar-container/div/"
                                                   "sidebar-view/div/div/div[1]/div/div[1]/div/span").text
            # print("TITLE FOUNDED!(2)")
        except:
            # print("----TITLE not found!----(conv_type)")
            pass
    if len(browser.find_elements(By.TAG_NAME, "modal-channel-info")) != 0 or title == 'اطلاعات کانال':
        c_type = "channel"
        print("\nChannel")
    elif len(browser.find_elements(By.TAG_NAME, "modal-chat-info")) != 0 or title == 'اطلاعات گروه':
        c_type = "group"
        print("\nGroup")
    else:
        c_type = "chat"
        print("\nChat")
    return c_type


def download_conv_messages(conv, browser, config_li, tabs_handles, c_type):
    messages = fetch_conv_messages(conv, browser, c_type, config_li[8])
    # cutting messages list according to config
    cut_of_value_founded = 0
    for message in messages:
        c_date = Message.get_date(message)
        c_date = Configs.jalali_to_gregorian(int(c_date[0]), int(c_date[1]), int(c_date[2]))
        c_date = datetime.date(int(c_date[0]), int(c_date[1]), int(c_date[2]))
        config_date = Configs.jalali_to_gregorian(int(config_li[11]), int(config_li[12]), int(config_li[13]))
        config_date = datetime.date(int(config_li[11]), int(config_li[12]), int(config_li[13]))
        if c_date >= config_date and cut_of_value_founded == 0:
            cut_of_value_founded = 1
            cut_off = messages.index(message)
            messages = messages[cut_off:]
            Message.current_date = Message.get_date(message)
    print('messages number:', len(messages))
    saved_msgs = []
    for message in messages:
        browser.execute_script("arguments[0].scrollIntoView();", message)
        file_name = Downloaders.download_media(browser, message, config_li, tabs_handles, config_li[5], config_li[6])
        current_msg = Message()
        current_msg.get_msg_contents(message, file_name)
        saved_msgs.append(current_msg)
    return saved_msgs


def generate_random_nums_set():
    set_of_numbers = set()
    while len(set_of_numbers) < 10000:
        set_of_numbers.add(random.randint(10000000, 99999999))
    return set_of_numbers


def save_convs_info(browser, config_li, phone_num, date_time_addition, msgs, channels, groups, chats):

    # get host name
    server_name = socket.gethostname()
    # read username and password of database from "db_user_pass.txt"
    # (db_username, db_password) = DB.get_db_user_pass()
    (db_username, db_password) = (server_name, "")
    #connect to database and return connection and cursor
    try:
        (conn, cur) = DB.connect_to_db(server_name, "REDownloader", db_username, db_password)
    except:
        print("Connection to database failed.")
    try:
        values = str((phone_num, date_time_addition, "R"))
        cur.execute("""insert into account values """ + values)
        # print("""insert into account values """ + values)
        print("data inserted into account successfully.")
    except:
        print("Account table data's didn't saved!")
        traceback.print_exc()

    try:
        msgs_df = Message.create_msgs_df(msgs)
        # this is a list of messages table's data types to create it (if it doesn't exist)
        msg_col_types = ["nchar(10)", "ntext", "nvarchar(50)", "nchar(10)", "ntext", "nvarchar(50)", "nvarchar(50)",
                         "nvarchar(50)", "nvarchar(50)"]
        #create messages table if it doesn't exist and insert msgs_df data into table row by row
        DB.my_to_sql(msgs_df, cur, "msgs", msgs_df.columns.tolist(), msg_col_types, needs_key=True)
    except:
        print("msgs table data's didn't saved!")
        traceback.print_exc()

    try:
        chats_df = Chat.create_chats_df(chats, phone_num)
        # print(chats_df.columns.tolist())
        chat_col_types = ["nvarchar(50)", "nvarchar(50)", "nvarchar(50)", "ntext", "ntext", "nvarchar(50)",
                          "nvarchar(50)", "nchar(10)", "nvarchar(50)"]
        DB.my_to_sql(chats_df, cur, "private_chat", chats_df.columns.tolist(), chat_col_types)
    except:
        print("Privat_chat table data's didn't saved!")
        traceback.print_exc()

    try:
        groups_df = Group.create_groups_df(groups, phone_num)
        # print(groups_df.columns.tolist())
        group_col_types = ["nvarchar(50)", "ntext", "ntext", "nchar(10)", "nvarchar(50)",
                           "nvarchar(50)", "nchar(10)", "nvarchar(50)"]
        DB.my_to_sql(groups_df, cur, "groups", groups_df.columns.tolist(), group_col_types)
    except:
        print("Groups table data's didn't saved!")
        traceback.print_exc()

    try:
        members = Group.build_members_list(groups, date_time_addition)
        members_df = Person.create_persons_df(members, phone_num)
        contact_col_types = ["nvarchar(50)", "nvarchar(50)", "nvarchar(50)", "ntext", "ntext",
                             "nvarchar(50)", "nchar(10)", "nvarchar(50)", "nvarchar(50)", "nvarchar(50)"]
        DB.my_to_sql(members_df, cur, "person", members_df.columns.tolist(), contact_col_types, needs_key=True)
    except:
        print("Person(group members) table data's didn't saved!")
        traceback.print_exc()

    try:
        channel_df = Channel.create_channels_df(channels, phone_num)
        # print(channel_df.columns.tolist())
        channel_col_types = ["nvarchar(50)", "ntext", "ntext", "nchar(10)", "ntext", "nvarchar(50)",
                             "nvarchar(50)", "nchar(10)", "nvarchar(50)"]
        DB.my_to_sql(channel_df, cur, "channels", channel_df.columns.tolist(), channel_col_types)
    except:
        print("Channels table data's didn't saved!")
        traceback.print_exc()

    try:
        if config_li[5] == "1":
            date_time_addition1 = date_time_addition.replace(":", "_")
            writer = pandas.ExcelWriter('R_' + str(phone_num) + '(' + date_time_addition1 + ')'
                                        + '.xlsx', engine='xlsxwriter')
            msgs_df.to_excel(writer, 'sheet1')
            chats_df.to_excel(writer, 'sheet2')
            groups_df.to_excel(writer, 'sheet3')
            channel_df.to_excel(writer, 'sheet4')
            members_df.to_excel(writer, 'sheet5')
            writer.save()
        else:
            writer = None
    except:
        print("Something occurred while creating 'EXEL' file.")
        writer = date_time_addition1 = date_time_addition.replace(":", "_")
        writer = pandas.ExcelWriter('R_' + str(phone_num) + '(' + date_time_addition1 + ')'
                                    + '.xlsx', engine='xlsxwriter')
    return writer, conn, cur


def get_conv_info_and_msgs(browser, config_li, date_time_addition, tabs_handles, phone_num, conv_num=0,
                           channels=None, groups=None, chats=None, msgs=None):
    if msgs is None:
        msgs = []
    if chats is None:
        chats = []
    if channels is None:
        channels = []
    if groups is None:
        groups = []
    if conv_num == 0:
        current_conv_num = 0
    else:
        current_conv_num = conv_num
    random_num_set = generate_random_nums_set()
    try:
        conv_list = get_conv_list(browser, conv_ul_xpath)
        try:
            conv_list2 = conv_list[current_conv_num:]
        except:
            conv_list2 = conv_list
        print("Capturing messages ... ")
        for i in conv_list2:
            rand_num = random_num_set.pop()
            conv_list = get_conv_list(browser, conv_ul_xpath)
            conv = conv_list[current_conv_num]
            current_conv_num = current_conv_num+1
            try:
                conv.click()
                if EC.number_of_windows_to_be(3):
                    browser.switch_to.window(browser.window_handles[0])
            except:
                # TODO
                # traceback.print_exc()
                if browser.find_elements(By.CSS_SELECTOR, "button[class = 'btn-icon rbico-close']"):
                    browser.back()
                    sleep(3)
                    conv.click()
                elif browser.find_elements(By.CSS_SELECTOR, "li[class = 'im_dialog_wrap active']"):
                    browser.find_element(By.CSS_SELECTOR, "li[class = 'im_dialog_wrap active']").click()
                else:
                    browser.refresh()
                    sleep(5)
                    conv_list = get_conv_list(browser, conv_ul_xpath)
                    conv_list[current_conv_num].click()

            sleep(1)
            c_type = conv_type(browser)
            if c_type == "channel":
                current_conv = Channel()
                current_conv.get_channel_info(browser, tabs_handles, config_li[10])
                id = hash(str(datetime.datetime.today()) + str(rand_num) + "\"" + current_conv.name + "\"")
                current_conv.set_channel_id(id, date_time_addition)
                current_conv.date_time_addition = date_time_addition
                channels.append(current_conv)
            if c_type == "group":
                current_conv = Group()
                current_conv = current_conv.get_group_info(browser, tabs_handles, config_li[10], config_li[14],
                                                           current_conv_num)
                id = hash(str(datetime.datetime.today()) + str(rand_num) + "\"" + current_conv.name + "\"")
                current_conv.set_group_id(id, date_time_addition)
                current_conv.date_time_addition = date_time_addition
                groups.append(current_conv)
            elif c_type == "chat":
                current_conv = Chat()
                current_conv.person = current_conv.person.get_person_info(browser, tabs_handles, config_li[9])
                id = hash(str(datetime.datetime.today()) + str(rand_num) + "\"" + current_conv.person.name + "\"")
                current_conv.set_chat_id(id, date_time_addition)
                chats.append(current_conv)
            else:
                current_conv = Chat()
                current_conv.ID = "ERROR"
                current_conv.date_time_addition = date_time_addition
                id = hash("0")
            browser.back()
            current_conv_msgs = download_conv_messages(conv, browser, config_li, tabs_handles, c_type)
            Message.set_conv_id(current_conv_msgs, id, date_time_addition, phone_num)
            for msg in current_conv_msgs:
                msgs.append(msg)
            print("Conversation number "+str(current_conv_num+1)+"'s info captured.")
        return channels, chats, groups, msgs, current_conv_num
    except:
        # traceback.print_exc()
        print("Something occurred while saving conversations!")
        # for i in range(len(conv_list)):
        while current_conv_num < len(conv_list)-1:
            print("Trying to continue ...")
            browser.refresh()
            sleep(5)
            channels, chats, groups, msgs, current_conv_num = get_conv_info_and_msgs(browser, config_li,
                                                                                     date_time_addition,
                                                                                     tabs_handles,
                                                                                     conv_num + 1,
                                                                                     channels, groups, chats, msgs)
        return channels, chats, groups, msgs, current_conv_num


def save_contacts_info(configs_list, contacts_info, cur, date_time_addition, phone_num, writer):
    try:
        contacts_df = Contacts_r.creat_contact_df(contacts_info, phone_num, date_time_addition)
        if configs_list[5] == "1":
            date_time_addition1 = date_time_addition.replace(":", "_")
            writer = pandas.ExcelWriter('R_' + str(phone_num) + '(' + date_time_addition1 + ')'
                                        + '.xlsx', engine='xlsxwriter')
            contacts_df.to_excel(writer, 'sheet5')
            writer.save()
    except:
        print("Error! Contacts data's didn't save in exel file.")
    server_name = socket.gethostname()
    (db_username, db_password) = (server_name, "")
    try:
        (conn, cur) = DB.connect_to_db(server_name, "REDownloader", db_username, db_password)
    except:
        print("Connection to database failed.")
    try:
        contact_col_types = ["nvarchar(50)", "nvarchar(50)", "nvarchar(50)", "ntext", "ntext",
                             "nvarchar(50)", "nchar(10)", "nvarchar(50)", "nvarchar(50)", "nvarchar(50)"]
        DB.my_to_sql(contacts_df, cur, "person", contacts_df.columns.tolist(), contact_col_types, needs_key=True)
        cur.commit()
    except:
        traceback.print_exc()
        print("Error! Contacts data's didn't save in database.")


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


def rubika_downloader(download_path, default_d_path, phone_num=None, state=None, browser=None, tabs_handles=None,
                      configs_list=None, conv_num=0):
    configs_list = []
    contacts_info = []
    date_time_addition = None
    writer = None
    conn = None
    cur = None
    phone_number = phone_num
    try:
        if phone_num is None:
            if Login.is_connected():
                browser = Login.set_browser(download_path, login_page_url)
                # opening downloads tab and back to rubika tab
                tabs_handles = Downloaders.open_downloads(browser)
                # state = "after opening browser"
            else:
                ok = "0"
                connected = False
                print("Please check your connection and press 1 to continue.\n>>>\t")
                while not connected or ok != "1":
                    ok = input()
                    connected = Login.is_connected()
                    sleep(5)
                rubika_downloader(download_path, default_d_path)
            download_path = get_dnld_path(download_path, default_d_path)

            sleep(3)
            while EC.url_matches(login_page_url):
                # print("before login")
                phone_number = Login.login(browser, phone_number_field_xpath, next_button_xpath, yes_button_xpath)
                # print("before sending code")
                Login.send_code(browser, code_field_Xpath, login_page_url, phone_number_field_xpath,
                                next_button_xpath, yes_button_xpath)
                if EC.url_matches("https://web.rubika.ir/") or not EC.url_contains("login"):
                    break
                sleep(5)
            # set configs
            configs = Configs()
            configs_list = configs.config()
            date_time_addition = str(datetime.datetime.today())
            state = "after login"
            # print(state)
        if state == "after login":
            channels, chats, groups, msgs, current_conv_num = get_conv_info_and_msgs(browser, configs_list,
                                                                                     date_time_addition,
                                                                                     tabs_handles, phone_number)
            state = "after getting msgs and convs info"
            # print(state)
        if state == "after getting msgs and convs info":
            try:
                (writer, conn, cur) = save_convs_info(browser, configs_list, phone_number, date_time_addition, msgs,
                                                      channels,
                                                      groups, chats)
                state = "after saving msgs and convs info"
            except:
                # traceback.print_exc()
                state = "after saving msgs and convs info"
            # print(state)
        if state == "after saving msgs and convs info":
            try:
                contacts_info = Contacts_r.get_contacts(browser, configs_list[10], tabs_handles)
            except ElementClickInterceptedException:
                browser.refresh()
                sleep(5)
                try:
                    contacts_info = Contacts_r.get_contacts(browser, configs_list[10], tabs_handles)
                except:
                    pass
            state = "after getting contacts"
            # print(state)
        if state == "after getting contacts":
            save_contacts_info(configs_list, contacts_info, cur, date_time_addition, phone_number,
                               writer)
        print("DATA EXTRACTED AND SAVED SUCCESSFULLY!\n\n")
    except:
        traceback.print_exc()
        try:
            if state is None:
                rubika_downloader(download_path, default_d_path, phone_num=phone_number)
            else:
                browser.refresh()
                sleep(5)
                rubika_downloader(download_path, default_d_path, phone_number, state, browser, tabs_handles,
                                  configs_list)
        except:
            # traceback.print_exc()
            print("\n<<ERROR>>\nUnknown error occurred.\nPlease start again.\n")
            rubika_downloader(download_path, default_d_path)


login_page_url = "https://web.rubika.ir/#/login"
phone_number_field_xpath = '/html/body/app-root/tab-login/div/div/div[2]/div[1]/div/div[3]/div[3]/input[1]'
next_button_xpath = '/html/body/app-root/tab-login/div/div/div[2]/div[1]/div/div[3]/button/div/div'
yes_button_xpath1 = '/html/body/div/app-root/app-modal-container/div/app-modal-view'
yes_button_xpath2 = '/div/div/div/app-confirm-custom/div/div[2]/button[2]/span'
yes_button_xpath = yes_button_xpath1 + yes_button_xpath2
code_field_Xpath = '/html/body/app-root/tab-login/div/div/div[2]/div[2]/div/div[4]/div/input'
conv_ul_xpath = "/html/body/div[1]/app-root/span/div[1]/div/rb-chats/div/div[2]/div/div[1]/ul[2]"
media_folders_path = "..\\RE_downloader_media\\"
# media_folders_path = account_medias_path + ""
# state = None
