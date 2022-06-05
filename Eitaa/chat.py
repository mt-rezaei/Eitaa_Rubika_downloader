import pandas


class Chat:
    def __init__(self, contact, ID):
        self.contact = contact
        self.ID = ID

    # def set_messages(self, messages):
    #     self.messages = messages

    def get_title(self):
        return self.contact.get_name()

    # def get_messages(self):
    #     return self.messages

    def get_contact(self):
        return self.contact

    def get_info_dict(self):
        return self.contact.get_info_dict()


def create_chats_df(list_of_chats, account):
    chats_dict = {"name": [], "phone_number": [], "id": [], "biography": [], "pro_picture_name": [], "conv_id": [],
                  "account": [], "app": [], "date_time_addition": []}
    for chat in list_of_chats:
        chats_dict["account"].append(account)
        chats_dict["app"].append('E')
        chats_dict["name"].append(chat.account.name)
        chats_dict["phone_number"].append(chat.account.phone)
        chats_dict["id"].append(chat.account.id)
        chats_dict["biography"].append(chat.account.bio)
        chats_dict["pro_picture_name"].append(chat.account.pro_pic)
        chats_dict["conv_id"].append(chat.ID)
        chats_dict["date_time_addition"].append(chat.account.date_time_addition)
    # print(chats_dict)
    current_conversation_msgs_df = pandas.DataFrame.from_dict(chats_dict)
    return current_conversation_msgs_df
