import pandas
from Rubika.Person_r import Person


class Chat:
    def __init__(self):
        self.person = Person()
        self.conv_id = ""
        # self.date_time_addition = ""

    def set_chat_id(self, conv_id, date_time_addition):
        self.conv_id = conv_id
        self.person.date_time_addition = date_time_addition

    @staticmethod
    def create_chats_df(list_of_chats, account):
        chats_dict = {"name": [], "phone_number": [], "id": [], "biography": [], "pro_picture_name": [], "conv_id": [],
                      "account": [], "app": [], "date_time_addition": []}
        for chat in list_of_chats:
            chats_dict["account"].append(account)
            chats_dict["app"].append('R')
            chats_dict["name"].append(chat.person.name)
            chats_dict["phone_number"].append(chat.person.phone)
            chats_dict["id"].append(chat.person.id)
            chats_dict["biography"].append(chat.person.bio)
            chats_dict["pro_picture_name"].append(str(chat.person.pro_pic))
            chats_dict["conv_id"].append(chat.conv_id)
            chats_dict["date_time_addition"].append(chat.person.date_time_addition)
        # print(chats_dict)
        chats_df = pandas.DataFrame.from_dict(chats_dict)
        return chats_df
