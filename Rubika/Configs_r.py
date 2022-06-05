# import datetime


class Configs:
    y_n_questions = ["Download photos?\n1.Yes\n2.No", "ِDownload videos?\n1.Yes\n2.No",
                     "Download files?\n1.Yes\n2.No", "Download voices?\n1.Yes\n2.No",
                     "Save group members info?\n1.Yes\n2.No",
                     "Export as exel file?:\n1.Yes\n2.No"]
    size_questions = ["maximum limit of videos(min):",
                      "maximum limit of files(MB):",
                      "maximum limit of voices(MB):"]
    num_questions = ["Total number of posts from channels:",
                     "Total number of profile pictures:",
                     "capture messages since(hijri)\nYear(yyyy):",
                     "Month(mm):", "Day(dd):", "Maximum group members to captures(0 = all):"]

    # configs[0.d_img, 1.d_film, 2.d_file, 3.d_voice, 4.d_group_members, 5.exel_output,
    #         6.max_film, 7.max_file, 8.max_voice(fake),
    #         9.num_of_channel_posts, 10.num_of_profile_pics, 11.year, 12.month, 13.day,
    #         14.num_of_group_members, 15.date(useful form of year, mon ...)]

    def config(self):
        try:
            pre_configs = Configs.read_configs()
            configs_title = ["Download photos", "ِDownload videos", "Download files", "Download voices",
                             "Save group members info", "Export as exel file", "maximum limit of videos(min)",
                             "maximum limit of files(KB)", "maximum limit of voices(KB)",
                             "Total number of posts from channels", "Total number of profile pictures",
                             "capture messages since(hijri)\nYear(yyyy)", "Month(mm)", "Day(dd)",
                             "Maximum group members to captures(0 = all)"]
            print("Current Setting:")
            for title in configs_title:
                index = configs_title.index(title)
                if index == 6:
                    try:
                        print(title + ": " + str(float(pre_configs[index])/1000))
                    except:
                        print(title + ": 0")
                else:
                    print(title+": " + pre_configs[index])
        except FileNotFoundError:
            pass
        while True:
            print("Use current setting?\n1.Yes\n2.No\n")
            ans = input(">>>\t")
            if ans == "1" or ans == "2":
                break
            else:
                print("This is an unaccepted response, enter a valid value.")
        try:
            while True:
                if ans == "1":
                    configs = self.read_configs()
                    break
                else:
                    configs = self.get_configs()
                    self.write_configs(configs)
                    break
        except FileNotFoundError:
            print("No saved config available. Please enter your desired config:\n")
            configs = self.get_configs()
            print("Saving configs ...")
            self.write_configs(configs)
            print("Config saved!")

        return configs

    @staticmethod
    def write_configs(conf_list):
        with open('config_file_r.txt', 'w') as file:
            for item in conf_list:
                file.write('%s\n' % item)

    @staticmethod
    def read_configs():
        configs = []
        with open('config_file_r.txt', 'r') as file:
            for line in file:
                # remove linebreak which is the last character of the string
                current_item = line[:-1]
                # add item to the list
                configs.append(current_item)
        return configs

    @classmethod
    def get_configs(cls):
        configs = []
        # fill configs from 0 to 5 (yes-no questions)
        for question in cls.y_n_questions:
            print(question)
            while True:
                answer = input()
                if answer == "1":
                    configs.append(int(answer))
                    break
                elif answer == "2":
                    configs.append(int(answer))
                    break
                else:
                    print("This is an unaccepted response, enter a valid value")
        # fill configs from 6 to 8 (questions about max size)
        for question in cls.size_questions:
            print(question)
            while True:
                try:
                    answer = float(input())
                    configs.append(answer * 1000)
                    break
                except ValueError:
                    print("This is an unaccepted response, enter a valid value")
        # fill configs from 9 to 14 (questions about number of things)
        for question in cls.num_questions:
            print(question)
            while True:
                try:
                    answer = int(input())
                    configs.append(answer)
                    break
                except ValueError:
                    print("This is an unaccepted response, enter a valid value")
        # gre_date = cls.jalali_to_gregorian(configs[11], configs[12], configs[13])
        # configs.append(datetime.date(gre_date[0], gre_date[1], gre_date[2]))
        return configs

    @staticmethod
    def gregorian_to_jalali(gy, gm, gd):
        g_d_m = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
        if gm > 2:
            gy2 = gy + 1
        else:
            gy2 = gy
        days = 355666 + (365 * gy) + ((gy2 + 3) // 4) - ((gy2 + 99) // 100) + ((gy2 + 399) // 400) + gd + g_d_m[gm - 1]
        jy = -1595 + (33 * (days // 12053))
        days %= 12053
        jy += 4 * (days // 1461)
        days %= 1461
        if days > 365:
            jy += (days - 1) // 365
            days = (days - 1) % 365
        if days < 186:
            jm = 1 + (days // 31)
            jd = 1 + (days % 31)
        else:
            jm = 7 + ((days - 186) // 30)
            jd = 1 + ((days - 186) % 30)
        return [jy, jm, jd]

    @staticmethod
    def jalali_to_gregorian(jy, jm, jd):
        jy = jy + 1595
        days = -355668 + (365 * jy) + ((jy // 33) * 8) + (((jy % 33) + 3) // 4) + jd
        if jm < 7:
            days += (jm - 1) * 31
        else:
            days += ((jm - 7) * 30) + 186
        gy = 400 * (days // 146097)
        days %= 146097
        if days > 36524:
            days -= 1
            gy += 100 * (days // 36524)
            days %= 36524
            if days >= 365:
                days += 1
        gy += 4 * (days // 1461)
        days %= 1461
        if days > 365:
            gy += ((days - 1) // 365)
            days = (days - 1) % 365
        gd = days + 1
        if (gy % 4 == 0 and gy % 100 != 0) or gy % 400 == 0:
            kab = 29
        else:
            kab = 28
        sal_a = [0, 31, kab, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        gm = 0
        while gm < 13 and gd > sal_a[gm]:
            gd -= sal_a[gm]
            gm += 1
        return [gy, gm, gd]
