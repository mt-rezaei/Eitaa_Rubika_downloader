from Rubika import main_rubika
from Eitaa import main_eitaa
default_d_path = "C:\\RE_downloader_media"


def first_page():
    f_list = [0, 0]
    # print("" + "< بسم الله الرحمن الرحیم >" + "\t\t\t\t\t\t\t\t\t\n")
    print("\n\n<rubika and Eitaa Downloader >\n")
    print("Default download path: " + default_d_path + "\n1.OK\n2.New path")
    while True:
        ans = input(">>>\t")
        if ans == "1":
            d_path = default_d_path
            break
        elif ans == "2":
            d_path = []
            while not d_path:
                d_path = input("Please enter the new path:\n>>>")
                d_path = d_path.replace("\\", "\\\\")
            break
        else:
            print("Please enter the number of desired item")

    print("1.Add new account" + "\n" + "2.View captured accounts")
    while True:
        f_list[0] = input(">>>\t")
        if f_list[0] == "1" or f_list[0] == "2":
            break
        else:
            print("Please enter the number of desired item")
    print("Choose messenger:")
    print("1.Eitaa")
    print("2.Rubika")
    while True:
        f_list[1] = input(">>>\t")
        if f_list[1] == "1" or f_list[1] == "2":
            break
        else:
            print("Please enter the number of desired item")
    return f_list, d_path


def main():
    while True:
        (option_list, d_path) = first_page()

        if option_list[0] == "1":
            if option_list[1] == "1":
                pass
                # add account to eitaa
                print("<Add Eitaa Account>")
                print("Please wait ...")
                main_eitaa.main(d_path, default_d_path)
            else:
                print("<Add Rubika Account>")
                print("Please wait ...")
                main_rubika.rubika_downloader(d_path, default_d_path)
                # add account to rubika
        else:
            if option_list[1] == "1":
                pass
                # DB.connect_to_db()
            else:
                pass
                # search in rubika s


if __name__ == '__main__':
    main()


phone_num = 0
