import datetime
from Eitaa import date_util


class Config_questions:
    questions = ["Download photos?\n1.Yes\n2.No", "ِDownload videos?\n1.Yes\n2.No",
                 "Download files?\n1.Yes\n2.No", "Download voices?\n1.Yes\n2.No",
                 "maximum limit of files(MB):",
                 "Total number of posts from channels:",
                 "Total number of profile pictures:",
                 "capture messages since(hijri):",
                 "Save group members info?\n1.Yes\n2.No",
                 "Total number of group members to save:",
                 "Export as exel file?:\n1.Yes\n2.No"]


def use_previous_config():
    arr2 = []
    with open('Eitaa/config.txt', 'r') as file:
        txt = file.read()
        arr = txt.split('#')
        arr2.append(int(arr[0]))
        arr2.append(int(arr[1]))
        arr2.append(int(arr[2]))
        arr2.append(int(arr[3]))
        arr2.append(int(arr[4]))
        arr2.append(int(arr[5]))
        arr2.append(int(arr[6]))

        date_arr = arr[7].split("/")
        y = int(date_arr[0]) + 2000
        m = int(date_arr[1])
        d = int(date_arr[2])
        yn, mn, dn = date_util.gregorian_to_jalali(y, m, d)
        date = datetime.datetime(yn, mn, dn)
        arr2.append(date)
        arr2.append(int(arr[8]))
        arr2.append(int(arr[9]))
        arr2.append(int(arr[10]))

    return arr2


def new_config():
    arr = []
    # 0 photoD  1 videoD  2 fileD  3 audioD  4 max_file  5 last_channel_posts  # 6 last_profiles
    # 7 date  8 save group members  9 how many group members  10 excel
    y_n_config(arr, 0)
    y_n_config(arr, 1)
    y_n_config(arr, 2)
    y_n_config(arr, 3)
    value_config(arr, 4)
    value_config(arr, 5)
    value_config(arr, 6)
    date_config(arr, 7)
    y_n_config(arr, 8)
    value_config(arr, 9)
    y_n_config(arr, 10)

    try:
        file = open("Eitaa/config.txt", "w")
        for i in range(len(arr)):
            if i == 7:
                file.write(arr[7].strftime("%y/%m/%d"))
            else:
                file.write(str(arr[i]))
            if i != len(arr) - 1:
                file.write('#')
        print("config saved!")
    except FileNotFoundError:
        print("No saved config available. Please enter your desired config:\n")
        return new_config()

    return arr


def date_config(arr, index):
    while True:
        try:
            print(Config_questions.questions[index])
            print("Enter date (hijri)")
            year = int(input("Year:"))
            month = int(input("Month:"))
            day = int(input("Day:"))
            gy, gm, gd = date_util.jalali_to_gregorian(year, month, day)
            date = datetime.datetime(gy, gm, gd)
            arr.append(date)
        except ValueError:
            print("Please enter the number of desired item.")
            continue
        else:
            break


def value_config(arr, index):
    while True:
        try:
            a = int(input(Config_questions.questions[index]))
            if index == 4:
                arr.append(a*1024)
            else:
                arr.append(a)
        except ValueError:
            print("Please enter the number of desired item.")
            continue
        else:
            break


def y_n_config(arr, index):
    while True:
        a = input(Config_questions.questions[index])
        if a == "1":
            arr.append(1)
            break
        elif a == "2":
            arr.append(0)
            break
        else:
            print("Please enter the number of desired item.")
            continue

