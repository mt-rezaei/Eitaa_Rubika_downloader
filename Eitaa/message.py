import datetime
import pandas
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import Eitaa.message
from Eitaa import date_util

y, m, d = date_util.jalali_to_gregorian(1396, 1, 1)
message_date = datetime.datetime(y, m, d)


class Message:

    def __init__(self, time, date, text, sender_name, media_name, conv_id, date_time_addition, phone_number):
        self.date = date
        self.time = time
        self.text = text
        self.media_name = media_name
        self.sender_name = sender_name
        self.conv_id = conv_id
        self.date_time_addition = date_time_addition
        self.phone_number = phone_number

    def get_time(self):
        return self.time

    def get_date(self):
        return self.date

    def get_text(self):
        return self.text

    def get_sender_name(self):
        return self.sender_name

    def get_media_name(self):
        return self.media_name

    def get_info_dict(self):
        data = {
            "time": self.time,
            "date": self.date,
            "text": self.text,
            "sender_name": self.sender_name,
            "media_name": self.media_name
        }
        return data


def find_text(message):
    try:
        text = message.find_element(By.CSS_SELECTOR, "div[class = 'im_message_outer_wrap hasselect']") \
            .find_element(By.CSS_SELECTOR, "div[class = 'im_message_body']") \
            .find_element(By.CSS_SELECTOR, "div[class = 'im_message_text']").text
    except NoSuchElementException:
        # print("doesnt have text")
        return "NULL"
    return text


def find_sender_name(message):
    sender_name = "NULL"
    try:
        sender_name = message.find_element(By.CLASS_NAME, "im_message_author_wrap")\
            .find_element(By.TAG_NAME, 'a').text
    except Exception:
        try:
            sender_name = message.find_element(By.CSS_SELECTOR, "div[class = 'im_message_outer_wrap hasselect']")\
                .find_element(By.CSS_SELECTOR, "div[class = 'im_message_body im_message_body_media']")\
                .find_element(By.CSS_SELECTOR, "span[class = 'im_message_author_wrap']")\
                .find_element(By.TAG_NAME, 'a').text

        except Exception:
            pass

    return sender_name


def find_time(message):
    time = "NULL"
    try:
        time_txt = message.find_element(By.CSS_SELECTOR, "div[class = 'im_message_outer_wrap hasselect']") \
            .find_element(By.CSS_SELECTOR, "div[class = 'im_message_meta pull-right text-right noselect']") \
            .find_element(By.CSS_SELECTOR, "span[class = 'im_message_date_text nocopy']") \
            .get_attribute("data-content")
        time_arr = time_txt.split(":")
        hour = int(time_arr[0])
        minute = int(time_arr[1])
        time = datetime.time(hour, minute)
        # print(time)
    except NoSuchElementException:
        pass
        # print("can not find time!!")
    return time


def find_date(msg):
    date = Eitaa.message.message_date
    try:
        date_string = msg. \
            find_element(By.CSS_SELECTOR,
                         "div[class = 'im_message_date_split im_service_message_wrap']") \
            .find_element(By.CSS_SELECTOR, "span[class = 'im_message_date_split_text']").text
        date = date_util.convert_string_to_date(date_string)
        if date is None or "":
            date = Eitaa.message.message_date
    except NoSuchElementException:
        # print("###################\n"+"can not find date")
        pass
    Eitaa.message.message_date = date
    return date


def create_msgs_dict(list_of_msgs):
    current_conversation_msgs_dict = {"gregorian_date": [], "m_text": [], "m_date": [], "m_time": [], "media_name": [],
                                      "sender_name": [], "conv_id": [], "date_time_addition": [], "phone_number": []}
    for message in list_of_msgs:
        yn, mn, dn = date_util.jalali_to_gregorian(message.date.year, message.date.month, message.date.day)
        s = str(yn)+"/"+str(mn)+"/"+str(dn)
        current_conversation_msgs_dict["gregorian_date"].append(s)
        current_conversation_msgs_dict["m_text"].append(message.text)
        current_conversation_msgs_dict["m_time"].append(str(message.time))
        current_conversation_msgs_dict["media_name"].append(message.media_name)
        current_conversation_msgs_dict["sender_name"].append(message.sender_name)
        # date_str = message.date.strftime("%d/%m/%y")
        current_conversation_msgs_dict["m_date"].append(str(message.date))
        current_conversation_msgs_dict["conv_id"].append(message.conv_id)
        current_conversation_msgs_dict["date_time_addition"].append(message.date_time_addition)
        current_conversation_msgs_dict["phone_number"].append(message.date_time_addition)

    return current_conversation_msgs_dict


def create_msgs_df(list_of_msgs):
    dict_of_msgs = create_msgs_dict(list_of_msgs)
    # print(dict_of_msgs)
    current_conversation_msgs_df = pandas.DataFrame.from_dict(dict_of_msgs)
    return current_conversation_msgs_df
