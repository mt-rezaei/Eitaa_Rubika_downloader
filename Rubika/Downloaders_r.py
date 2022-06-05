from time import sleep, time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, \
    ElementNotInteractableException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains


class Downloaders:

    @staticmethod
    def open_downloads(browser):
        browser.execute_script("window.open()")
        tabs_handles = browser.window_handles
        WebDriverWait(browser, 10).until(EC.new_window_is_opened)
        browser.switch_to.window(browser.window_handles[-1])
        browser.get("about:downloads")
        browser.switch_to.window(browser.window_handles[0])
        return tabs_handles

    @classmethod
    def get_downloaded_file_name(cls, wait_time, browser, tabs_handles):
        browser.switch_to.window(tabs_handles[1])
        end_time = time() + wait_time
        while True:
            try:
                file_name = browser.execute_script("return document.querySelector"
                                                   "('#contentAreaDownloadsView .downloadMainArea "
                                                   ".downloadContainer description:nth-of-type(1)').value")
                if file_name:
                    browser.switch_to.window(tabs_handles[0])
                    sleep(3)
                    return file_name
            except:
                pass
            sleep(1)
            if time() > end_time:
                # browser.execute_script("window.close()")
                browser.switch_to.window(tabs_handles[0])
                sleep(3)
                return "<No file>"

    @classmethod
    def download_image(cls, browser, download_image_, css_selector, tabs_handles, msg_element=None):
        try:
            if download_image_:
                # profile.set_preference("browser.download.dir", medias_path + "images")
                if msg_element is None:
                    img = browser.find_element(By.CSS_SELECTOR, css_selector)
                else:
                    img = msg_element.find_element(By.CSS_SELECTOR, "div[class = 'attachment media-container']") \
                        .find_element(By.CSS_SELECTOR, "img[class = 'media-photo thumbnail']")
                img.click()
                sleep(1)
                browser.find_element(By.CSS_SELECTOR, 'button[class = "btn-icon rbico-download rp"]'). \
                    find_element(By.CSS_SELECTOR, 'div[class = "c-ripple rp"]').click()
                sleep(3)
                browser.find_element(By.CSS_SELECTOR, 'button[class = "btn-icon rbico-close"]').click()
                file_name = cls.get_downloaded_file_name(5, browser, tabs_handles)
                # print(file_name)
                print('image downloaded.')
                return file_name
            else:
                browser.find_element(By.XPATH, 'a')
        except (NoSuchElementException, ElementClickInterceptedException):
            return "0"

    @classmethod
    def download_video(cls, browser, download_videos_, msg_element, tabs_handles, max_video_size=1000):
        try:
            time = msg_element.find_element(By.CSS_SELECTOR, "div[class = 'attachment media-container']") \
                .find_element(By.CSS_SELECTOR, "span[class = 'video-time']").text
            time = time.split(":")
            time = time[0]
            try:
                time = float(time)
            except:
                time = 0
            if download_videos_ and float(time) <= float(max_video_size) / 1000:
                button = msg_element.find_element(By.CSS_SELECTOR, "div[class = 'attachment media-container']") \
                    .find_element(By.CSS_SELECTOR, "span[class = 'video-play rbico-largeplay btn-circle "
                                                   "position-center']")
                # .find_element(By.CSS_SELECTOR, "img[class = 'media-photo']")
                while True:
                    action = ActionChains(browser)
                    action.context_click(button).perform()
                    sleep(1)
                    try:
                        dnld_action = ActionChains(browser)
                        dnld_button = browser.find_element(By.CSS_SELECTOR, "div[class = 'btn-menu contextmenu "
                                                                            "bottom-right active']") \
                            .find_element(By.CSS_SELECTOR, "div[class = 'btn-menu-item rbico-download rp']") \
                            .find_element(By.CSS_SELECTOR, "div[class = 'c-ripple rp']")
                        dnld_action.double_click(dnld_button).perform()
                        sleep(2)
                        break
                    except ElementNotInteractableException:
                        continue

                sleep(2)
                file_name = cls.get_downloaded_file_name(30, browser, tabs_handles)
                # print(file_name)
                print('video downloaded.')
                return file_name
            else:
                browser.find_element(By.XPATH, 'a')
        except (NoSuchElementException, ElementClickInterceptedException):
            return "0"

    @staticmethod
    def size_to_kb(size_string):
        size = size_string[:-2]
        size_m = size_string[-2:]
        if size_m == "GB":
            try:
                size = float(size) * 1000000
            except ValueError:
                size = 0
            # print(size)
        elif size_m == "MB":
            try:
                size = float(size) * 1000
            except ValueError:
                size = 0
            # print(size)
        elif size_m == "KB":
            try:
                size = float(size)
            except ValueError:
                size = 0
            # print(size)
        else:
            try:
                size = float(size_string[-1]) * 0.001
            except (ValueError, IndexError):
                size = 0
            # print(size)
        return size

    @classmethod
    def download_file(cls, browser, download_files_, msg_element, tabs_handles, max_file_size=1000):
        try:
            size = msg_element.find_element(By.CSS_SELECTOR, "div[class = 'document-size']").text
            size = Downloaders.size_to_kb(size)
            if download_files_ and size <= float(max_file_size):
                button = msg_element.find_element(By.TAG_NAME, "rb-message-file-doc")
                while True:
                    action = ActionChains(browser)
                    action.context_click(button).perform()
                    sleep(1)
                    try:
                        dnld_action = ActionChains(browser)
                        dnld_button = browser.find_element(By.CSS_SELECTOR, "div[class = 'btn-menu contextmenu "
                                                                            "bottom-right active']") \
                            .find_element(By.CSS_SELECTOR, "div[class = 'btn-menu-item rbico-download rp']") \
                            .find_element(By.CSS_SELECTOR, "div[class = 'c-ripple rp']")
                        dnld_action.double_click(dnld_button).perform()
                        sleep(2)
                        break
                    except ElementNotInteractableException:
                        continue
                file_name = cls.get_downloaded_file_name(20, browser, tabs_handles)
                # print(file_name)
                print('file downloaded.')
                return file_name
            else:
                browser.find_element(By.XPATH, 'a')
        except (NoSuchElementException, ElementClickInterceptedException):
            return "0"

    @classmethod
    def download_voice(cls, browser, download_voices_, message_element, tabs_handles):
        try:
            if download_voices_:
                button = message_element.find_element(By.TAG_NAME, "rb-message-audio-player")
                while True:
                    action = ActionChains(browser)
                    action.context_click(button).perform()
                    sleep(1)
                    try:
                        dnld_action = ActionChains(browser)
                        dnld_button = browser.find_element(By.CSS_SELECTOR, "div[class = 'btn-menu contextmenu "
                                                                            "bottom-right active']") \
                            .find_element(By.CSS_SELECTOR, "div[class = 'btn-menu-item rbico-download rp']") \
                            .find_element(By.CSS_SELECTOR, "div[class = 'c-ripple rp']")
                        dnld_action.double_click(dnld_button).perform()
                        sleep(2)
                        break
                    except ElementNotInteractableException:
                        continue
                file_name = cls.get_downloaded_file_name(15, browser, tabs_handles)
                # print(file_name)
                print('voice message downloaded.')
                return file_name
            else:
                browser.find_element(By.XPATH, 'a')
        except NoSuchElementException:
            return "0"

    @classmethod
    def download_media(cls, browser, msg, option, tabs_handles, video_size, file_size):
        css_selector = 'a[class = "im_message_photo_thumb relative"]'
        file_names = [cls.download_image(browser, option[0], css_selector, tabs_handles, msg),
                      cls.download_video(browser, option[1], msg, tabs_handles, video_size),
                      cls.download_voice(browser, option[2], msg, tabs_handles),
                      cls.download_file(browser, option[3], msg, tabs_handles, file_size)]
        for file_name in file_names:
            if file_name != "0":
                return file_name
        return "NULL"

    @classmethod
    def download_pro_pic(cls, browser, tabs_handles, profile_num=3):
        pro_pics = []
        try:
            browser.find_element(By.CSS_SELECTOR, "div[class = 'profile-avatars-avatar media-container']").click()
            sleep(2)
        except (NoSuchElementException, ElementNotInteractableException):
            return "NULL"
        for pic in range(int(profile_num) + 1):
            browser.find_element(By.CSS_SELECTOR, "button[class = 'btn-icon rbico-download rp']"). \
                find_element(By.CSS_SELECTOR, "div[class = 'c-ripple rp']").click()
            pro_pics.append(cls.get_downloaded_file_name(10, browser, tabs_handles))
            try:
                browser.find_element(By.CSS_SELECTOR, "div[class = 'media-viewer-switcher "
                                                      "media-viewer-switcher-right']").click()
                sleep(2)
            except (NoSuchElementException, ElementClickInterceptedException):
                try:
                    browser.find_element(By.XPATH,
                                         "/html/body/app-root/div/page-container/slider-view/div/"
                                         "modal-photo-slider/div[3]").click()
                except:
                    pass
                try:
                    browser.find_element(By.XPATH,
                                         "/html/body/app-root/div/page-container/slider-view/div/"
                                         "modal-photo-slider/div[4]/div[2]/button[2]").click()
                except ElementClickInterceptedException:
                    browser.back()
                if pro_pics:
                    pro_pic_str = "["
                    for name in pro_pics:
                        pro_pic_str = pro_pic_str + name + ", "
                    pro_pic_str = pro_pic_str[:-1]
                    return pro_pic_str + "]"
                else:
                    return "NUll"
        # try:
        #     browser.find_element(By.XPATH, "/html/body/div[1]/app-root/app-modal-container/div/app-modal-view[2]/"
        #                                    "div/div/div/modal-photo-slider/div[3]/div").click()
        # except ElementClickInterceptedException:
        #     browser.back()
        # return pro_pics
