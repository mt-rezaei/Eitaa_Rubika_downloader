import datetime
import pandas
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from Rubika.Configs_r import Configs


class Message:
    def __init__(self):
        self.gregorian_date = ""
        self.text = ""
        self.date = ""
        self.time = ""
        self.media_name = ""
        self.sender_name = ""
        self.conv_ID = ""
        self.date_time_addition = ""
        self.phone_number = ""

    current_date = [2018, 3, 20]
    current_time = datetime.time(0, 0)

    def get_msg_contents(self, msg, file_name):
        self.time = self.get_time(msg)
        # print(self.time)
        date_list = self.get_date(msg)
        self.date = str(date_list[0])+"-"+str(date_list[1])+"-"+str(date_list[2])
        g_date_list = Configs.jalali_to_gregorian(date_list[0], date_list[1], date_list[2])
        self.gregorian_date = str(g_date_list[0])+"-"+str(g_date_list[1])+"-"+str(g_date_list[2])
        try:
            self.sender_name = msg.find_element(By.CSS_SELECTOR, "a[class = 'name peer-title user_color_1']").text
        except:
            self.sender_name = "NULL"
        try:
            self.text = msg.find_element(By.CSS_SELECTOR, "div[class = 'bubble-content']")\
                .find_element(By.CSS_SELECTOR, "div[class = 'message']").text
        except NoSuchElementException:
            self.text = "NULL"
        self.media_name = file_name
        return self

    @classmethod
    def get_time(cls, msg):
        try:
            new_time = msg.find_element(By.CSS_SELECTOR, "span[class = 'time rbico']").\
                get_attribute("title")
            new_time = new_time.split(":")
            new_time = datetime.time(int(new_time[0]), int(new_time[1]))
            cls.current_time = new_time
        except NoSuchElementException:
            new_time = cls.current_time
        return new_time

    @classmethod
    def get_date(cls, msg):
        """returns a list of integers: [yyyy, mm, dd] """
        try:
            date_text = msg.find_element(By.CSS_SELECTOR, "div[class = 'bubble-content']")\
                .find_element(By.CSS_SELECTOR, "div[class = 'service-msg']")\
                .find_element(By.TAG_NAME, "span").text
            date_text = date_text.split("،")

            date_text = date_text[1].split(" ")
            date_text = date_text[1:]
            date_text[1] = str(cls.mtxt_to_num(date_text[1]))
            new_date = [int(date_text[2]), int(date_text[1]), int(date_text[0])]
            cls.current_date = new_date
            return new_date
        except (NoSuchElementException, StaleElementReferenceException, IndexError):
            return cls.current_date

    @staticmethod
    def mtxt_to_num(name):
        months = ["فروردین", "اردیبهشت", "خرداد",
                  "تیر", "مرداد", "شهریور",
                  "مهر", "آبان", "آذر",
                  "دی", "بهمن", "اسفند"]
        try:
            return months.index(name) + 1
        except ValueError:
            # print("error in months method.")
            return 0

    @staticmethod
    def set_conv_id(list_of_msgs, conv_id, date_time_addition, phone_num):
        for msg in list_of_msgs:
            msg.conv_ID = conv_id
            msg.date_time_addition = date_time_addition
            msg.phone_number = phone_num

    @staticmethod
    def create_msgs_dict(list_of_msgs):
        msgs_dict = {"gregorian_date": [], "m_text": [], "m_date": [], "m_time": [], "media_name": [],
                     "sender_name": [], "conv_id": [],
                     "date_time_addition": [], "phone_number": []}
        for message in list_of_msgs:
            msgs_dict["gregorian_date"].append(message.gregorian_date)
            msgs_dict["m_text"].append(message.text)
            msgs_dict["m_time"].append(str(message.time))
            msgs_dict["media_name"].append(message.media_name)
            msgs_dict["sender_name"].append(message.sender_name)
            msgs_dict["m_date"].append(str(message.date))
            msgs_dict["conv_id"].append(message.conv_ID)
            msgs_dict["date_time_addition"].append(message.date_time_addition)
            msgs_dict["phone_number"].append(message.phone_number)
        return msgs_dict

    @staticmethod
    def create_msgs_df(list_of_msgs):
        dict_of_msgs = Message.create_msgs_dict(list_of_msgs)
        # print(dict_of_msgs)
        msgs_df = pandas.DataFrame.from_dict(dict_of_msgs)
        return msgs_df
    #TODO

    def creat_msg_tpl(self):
        msgs_dict = (self.text, self.date, self.time, self.media_name, self.sender_name, self.conv_ID)
