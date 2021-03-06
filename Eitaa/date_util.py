import datetime


def jalali_to_gregorian(jy, jm, jd):
    jy += 1595
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
    if (gy % 4 == 0 and gy % 100 != 0) or (gy % 400 == 0):
        kab = 29
    else:
        kab = 28
    sal_a = [0, 31, kab, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    gm = 0
    while gm < 13 and gd > sal_a[gm]:
        gd -= sal_a[gm]
        gm += 1
    return gy, gm, gd


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


def convert_string_to_date(date_string):
    if date_string is not "":
        date_string = str(date_string)
        date_string = date_string.split(",")[-1]
        arr = date_string.split(" ")
        day_txt = arr[1]

        day_arr = list(day_txt)
        day_txt_en = ""
        for d in day_arr:
            day_txt_en = day_txt_en + per_to_en(d)
        day = int(day_txt_en)

        month_txt = arr[2]
        month = get_month(month_txt)

        year_txt = arr[3]
        year_arr = list(year_txt)
        year_txt_en = ""
        for y in year_arr:
            year_txt_en = year_txt_en + per_to_en(y)
        year = int(year_txt_en)

        # yn, mn, dn = jalali_to_gregorian(year, month, day)
        return datetime.datetime(year, month, day)
    return None


def per_to_en(num_string):
    persion = ['??', '??', '??', '??', '??', '??', '??', '??', '??', '??']
    english = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    for p in persion:
        if num_string == p:
            return english[persion.index(p)]
    return None


def get_month(month):
    months = ["??????????????", "????????????????", "??????????", "??????", "??????????", "????????????",
              "??????", "????????", "??????", "????", "????????", "??????????"]
    try:
        return months.index(month) + 1
    except ValueError:
        return None
