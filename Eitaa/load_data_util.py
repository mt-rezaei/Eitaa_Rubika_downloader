import datetime
import random
import socket
from time import sleep

import pandas
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from DB import DB
from Eitaa import chat
from Eitaa import downloader, channel
from Eitaa import group
from Eitaa import message
from Eitaa import person

all_messages = []


def get_all_chats(driver):
    sleep(3)
    html_list = driver.find_element(By.XPATH, "/html/body/div[1]/div[2]/div/div[1]/div[2]/div/div[1]/ul")
    chats = html_list.find_elements(By.TAG_NAME, "a")
    return chats


def generate_random_nums_set():
    set_of_numbers = set()
    while len(set_of_numbers) < 10000:
        set_of_numbers.add(random.randint(10000000, 99999999))
    return set_of_numbers


def analyze_message(msg, driver, config_arr, tabs_handles, conv_id, date_time_addition, phone_number):
    driver.execute_script("return arguments[0].scrollIntoView();", msg)
    caption = ""
    flag = 0
    date = message.find_date(msg)
    time = message.find_time(msg)
    text = message.find_text(msg)
    if text is not None or text != "":
        flag = 1
        # print(text)
    sender_name = message.find_sender_name(msg)
    media_name, caption = downloader.download(msg, driver, flag, config_arr, tabs_handles)
    if caption != "":
        text = caption
    analyzed_message = message.Message(time, date, text, sender_name, media_name, conv_id,
                                       date_time_addition, phone_number=phone_number)
    # print(analyzed_message.get_info_dict())
    return analyzed_message


def analyze_messages(messages, driver, config_arr, tabs_handles, conv_id, date_time_addition, phone_number):
    analyzed_messages = []
    for m in messages:
        if m.is_displayed():
            am = analyze_message(m, driver, config_arr, tabs_handles, conv_id, date_time_addition, phone_number)
            analyzed_messages.append(am)
    return analyzed_messages


def scroll_up_messages(driver):
    element = driver.find_element(
        By.XPATH, '/html/body/div[1]/div[2]/div/div[2]/div[3]/div/div[1]/div[1]/div/div[1]/div[2]/div[1]')
    driver.execute_script("return arguments[0].scrollIntoView();", element)


def get_conv_info(conv, driver, tabs_handles, config_arr, date_time_addition):
    random_num_set = generate_random_nums_set()
    rand_num = random_num_set.pop()
    wait = WebDriverWait(driver, 10)
    chat_type = get_conv_type(conv, driver, wait)

    # conversation = None
    if chat_type == "اطلاعات گروه":
        print("\nGroup")
        photos = downloader.get_photos(driver, tabs_handles)
        conversation = group.get_group_info(driver, photos, tabs_handles,
                                            config_arr, rand_num, date_time_addition)
        id = conversation.ID
        flag = 1

    elif chat_type == "اطلاعات مخاطب":
        print("\nChat")
        name, username, phone, profiles, bio = person.get_person_info(driver, config_arr, tabs_handles)
        p = person.Person(phone, profiles, name, username, bio, date_time_addition)
        id = str(hash(str(datetime.datetime.today()) + str(rand_num) + p.name))
        conversation = chat.Chat(p, id)
        flag = 2

    else:  # chat_type == "اطلاعات کانال":
        print("\nChannel")
        # photos = downloader.get_photos(driver, tabs_handles)
        photos = "NULL"
        conversation = channel.get_channel_info(driver, photos, rand_num, date_time_addition)
        id = conversation.id
        flag = 0

    # print(flag)
    try_to_close_conv_info(driver, wait)
    return conversation, flag, id


def get_conv_type(conv, driver, wait):
    wait.until(ec.element_to_be_clickable(conv.find_element(By.XPATH,
                                                            "/html/body/div[1]/div[1]/div/div"
                                                            "/div[2]/div/div[2]/a"))).click()

    sleep(2)
    chat_type = ''
    try:
        try:
            chat_type = driver.find_element(By.CSS_SELECTOR, "div[class= 'modal-content modal-content-animated']") \
                .find_element(By.CLASS_NAME, "md_modal_title").text
        except NoSuchElementException:
            chat_type = driver.find_element(By.XPATH,
                                            "/html/body/div[7]/div[2]/div/div/div[1]/div[1]/div[2]").text

    except NoSuchElementException:
        pass
    # print(chat_type)
    return chat_type


def try_to_close_conv_info(driver, wait):
    try:
        sleep(2)
        wait.until(ec.element_to_be_clickable(driver.find_element(
            By.CSS_SELECTOR, "div[class = 'modal_close_wrap']"))).click()
    except Exception:
        try:
            sleep(2)
            wait.until(ec.element_to_be_clickable(driver.find_element(By.XPATH,
                                                                      "/html/body/div[5]/div[1]"))).click()
        except Exception:
            try:
                sleep(2)
                wait.until(ec.element_to_be_clickable(driver.find_element(
                    By.CSS_SELECTOR, "a[class = 'md_modal_action md_modal_action_close']"))).click()
            except Exception:
                try:
                    sleep(2)
                    b = driver.find_element_by_xpath("/html/body/div[5]/div[2]/div/div/div[1]/div[1]/div[1]/a")
                    driver.execute_script("arguments[0].click();", b)
                except Exception:
                    try:
                        sleep(2)
                        driver.find_element(By.XPATH,
                                            "/html/body/div[5]/div[2]/div/div/div[1]/div[1]/div[1]/a").click()
                    except Exception:
                        close = driver.find_element(By.XPATH, "/html/body/div[5]")
                        action = ActionChains(driver)
                        action.move_to_element_with_offset(close, 20, 20)
                        action.click()
                        action.perform()
    sleep(2)


def eitaa_downloader(driver, config_arr, tabs_handles, phone_number,
                     date_time_addition, channels, groups, chats):
    sleep(3)
    try:
        convs = get_all_chats(driver)
    except Exception:
        convs = get_all_chats(driver)

    # todo
    # convs = convs[1:2]
    print("Capturing messages ... ")

    for c in range(len(convs)):
        try:
            try:
                get_all_conv_messages(channels, chats, config_arr,
                                      convs[c], date_time_addition, driver, groups, tabs_handles, phone_number)
            except Exception:
                get_all_conv_messages(channels, chats, config_arr,
                                      convs[c], date_time_addition, driver, groups, tabs_handles, phone_number)
        except Exception:
            continue

    print("DATA EXTRACTED AND SAVED SUCCESSFULLY!\n\n")
    return channels, chats, groups, phone_number


def get_all_conv_messages(channels, chats, config_arr, conv, date_time_addition, driver,
                          groups, tabs_handles, phone_number):
    driver.execute_script("arguments[0].scrollIntoView();", conv)
    conv.click()
    sleep(3)
    conversation, flag, conv_id = get_conv_info(conv, driver, tabs_handles,
                                                config_arr, date_time_addition)
    messages = load_messages(driver, flag, config_arr)
    # print("############################")
    # print(len(messages))
    analyzed_messages = analyze_messages(messages, driver, config_arr,
                                         tabs_handles, conv_id, date_time_addition, phone_number)
    if flag == 0:
        if len(analyzed_messages) >= config_arr[5]:
            analyzed_messages = analyzed_messages[-config_arr[5]:]
    # filter by date
    filtered_messages_by_date = []
    start_date = config_arr[7]
    for msg in analyzed_messages:
        if msg.get_date() > start_date:
            filtered_messages_by_date.append(msg)
    all_messages.extend(filtered_messages_by_date)
    if flag == 0:
        channels.append(conversation)
    elif flag == 1:
        groups.append(conversation)
    elif flag == 2:
        chats.append(conversation)


def save_information(channels, chats, contacts, groups, phone_number, date_time_addition, config_arr):
    date_time_addition1 = date_time_addition.replace(":", "_")
    writer = pandas.ExcelWriter('R_' + str(phone_number) + "(" + date_time_addition1 + ")" + '.xlsx',
                                engine='xlsxwriter')

    server_name = socket.gethostname()
    (db_username, db_password) = (server_name, "")
    try:
        (conn, cur) = DB.connect_to_db(server_name, "REDownloader", db_username, db_password)
    except:
        print("Connection to database failed.")
    try:
        msgs_df = message.create_msgs_df(all_messages)
        msgs_df.to_excel(writer, 'sheet1')
        msg_col_types = ["nchar(10)", "ntext", "nvarchar(50)", "nchar(10)", "ntext", "nvarchar(50)", "nvarchar(50)",
                         "nvarchar(50)", "nvarchar(50)"]
        DB.my_to_sql(msgs_df, cur, "msgs", msgs_df.columns.tolist(), msg_col_types, needs_key=True)
    except Exception:
        print("Messages table data's didn't saved!")

    try:
        chats_df = chat.create_chats_df(chats, phone_number)
        chats_df.to_excel(writer, 'sheet2')
        chat_col_types = ["nvarchar(50)", "nvarchar(50)", "nvarchar(50)", "ntext", "ntext",
                          "nvarchar(50)", "nvarchar(50)", "nchar(10)", "nvarchar(50)"]
        DB.my_to_sql(chats_df, cur, "private_chat", chats_df.columns.tolist(), chat_col_types)
    except Exception:
        print("Privat_chat table data's didn't saved!")

    try:
        groups_df = group.create_groups_df(groups, phone_number)
        groups_df.to_excel(writer, 'sheet3')
        group_col_types = ["nvarchar(50)", "ntext", "ntext", "nchar(10)",
                           "nvarchar(50)", "nvarchar(50)", "nchar(10)", "nvarchar(50)"]
        DB.my_to_sql(groups_df, cur, "groups", groups_df.columns.tolist(), group_col_types)
    except Exception:
        print("Groups table data's didn't saved!")

    try:
        channels_df = channel.create_channels_df(channels, phone_number)
        channels_df.to_excel(writer, 'sheet4')
        channel_col_types = ["nvarchar(50)", "ntext", "ntext", "nchar(10)",
                             "ntext", "nvarchar(50)", "nvarchar(50)", "nchar(10)", "nvarchar(50)"]
        DB.my_to_sql(chats_df, cur, "channels", channels_df.columns.tolist(), channel_col_types)
    except Exception:
        print("Channels table data's didn't saved!")

    try:
        members = group.build_members_list(groups)
        persons_df = person.create_persons_df(members, contacts, phone_number)
        persons_df.to_excel(writer, 'sheet5')
        contact_col_types = ["nvarchar(50)", "nvarchar(50)", "nvarchar(50)", "ntext", "ntext", "nvarchar(50)",
                             "nchar(10)", "nvarchar(50)", "nvarchar(50)", "nvarchar(50)"]
        DB.my_to_sql(persons_df, cur, "person", persons_df.columns.tolist(), contact_col_types, needs_key=True)
    except Exception:
        print("Person(group members and contacts) table data's didn't saved!")

    cur.commit()

    values = str((phone_number, date_time_addition, "E"))
    cur.execute("""insert into account values """ + values)
    cur.commit()

    if config_arr[10] == 1:
        writer.save()


def load_messages(driver, type_flag, config_arr):
    messages = driver.find_element(By.CSS_SELECTOR, "div[class = 'im_history_col']") \
        .find_elements(By.XPATH, '//div[@class="im_history_messages_peer ng-scope"]/div')

    current_messages_date = driver.find_elements(By.CSS_SELECTOR,
                                                 "span[class = 'im_message_date_split_text']")
    counter = 0
    all_messages_are_loaded = False

    f = False
    while not all_messages_are_loaded:

        # if it is channel, load only a few messages
        config_channel = config_arr[5]
        if type_flag == 0 and len(messages) >= config_channel:
            for i in range(1, len(messages)+1):
                try:
                    date_string = messages[-i]. \
                        find_element(By.CSS_SELECTOR,
                                     "div[class = 'im_message_date_split im_service_message_wrap']") \
                        .find_element(By.CSS_SELECTOR, "span[class = 'im_message_date_split_text']")
                    flag = True
                except Exception:
                    flag = False
                if flag and i >= config_channel:
                    config_channel = i
                    f = True
            if f:
                messages = messages[-config_channel:]
                break

        scroll_up_messages(driver)
        previous_messages_date = current_messages_date
        current_messages_date = driver.find_elements(By.CSS_SELECTOR, "span[class = 'im_message_date_split_text']")

        messages = driver.find_element(By.CSS_SELECTOR, "div[class = 'im_history_col']") \
            .find_elements(By.XPATH, '//div[@class="im_history_messages_peer ng-scope"]/div')

        if current_messages_date == previous_messages_date and counter >= 5:
            all_messages_are_loaded = True
        else:
            sleep(1)
            counter += 1
    scroll_up_messages(driver)
    print('messages number:', len(messages))
    return messages
