from time import sleep, time
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys


def download(message, driver, flag, config_arr, tabs_handles):
    media_name = None
    caption = ""
    sleep(2)
    wait = WebDriverWait(driver, 10)
    try:
        media_name, caption = photo_download(driver, message, wait, config_arr, tabs_handles)
    except NoSuchElementException:

        try:
            media_name = video_download(driver, message, wait, config_arr, tabs_handles)
        except NoSuchElementException:

            try:
                media_name = file_download(driver, message, wait, config_arr, tabs_handles)
            except NoSuchElementException:

                try:
                    media_name = audio_download(driver, message, wait, config_arr, tabs_handles)
                except NoSuchElementException:
                    pass
    return media_name, caption


def audio_download(driver, message, wait, config_arr, tabs_handles):
    file_name = None
    if config_arr[3] == 1:

        size_string = message.find_element(By.CSS_SELECTOR, "div[class = 'audio_player_title_wrap']") \
            .find_element(By.CSS_SELECTOR, "span[class = 'audio_player_size ng-binding ng-scope']").text
        size = extract_size(size_string)

        if size <= config_arr[4]:
            wait.until(ec.element_to_be_clickable
                       (message.find_element
                        (By.CSS_SELECTOR, "div[class = 'audio_player_actions noselect ng-scope']")
                        .find_element(By.CSS_SELECTOR, "a[class ='nocopy ng-scope']"))).click()
            file_name = get_downloaded_file_name(5, driver, tabs_handles)
            print("Download audio or voice message")
    return file_name


def file_download(driver, message, wait, config_arr, tabs_handles):
    file_name = None
    if config_arr[2] == 1:
        sleep(1)
        size_string = message.find_element(By.CSS_SELECTOR, "div[class = 'im_message_media "
                                                            "ng-scope ng-isolate-scope']") \
            .find_element(By.CSS_SELECTOR, "div[class = 'im_message_document_info']") \
            .find_element(By.CSS_SELECTOR, "span[class = 'im_message_document_size ng-binding ng-scope']").text
        size = extract_size(size_string)

        # if file is PDF ignore it! (can not download pdf files)
        file_type = message.find_element(By.CSS_SELECTOR, "div[class = 'im_message_document_info']")\
            .find_element(By.CSS_SELECTOR, "a[class = 'im_message_document_name']").get_attribute("data-ext")
        if file_type == ".pdf":
            return file_name

        if size <= config_arr[4]:
            wait.until(ec.element_to_be_clickable(
                message.find_element(By.CSS_SELECTOR, "div[class = 'im_message_media ng-scope ng-isolate-scope']")
                .find_element(By.CSS_SELECTOR, "div[class = 'im_message_document clearfix ng-scope']")
                .find_element(By.CSS_SELECTOR, "a[class = 'nocopy ng-scope']"))).click()
            sleep(1)
            e = message.find_element(By.CSS_SELECTOR, "div[class = 'im_message_document_actions ng-scope']") \
                .find_element(By.CSS_SELECTOR, "a[class ='nocopy ng-scope']")
            while True:
                if e.get_attribute("data-content") == "ذخیره":
                    wait.until(ec.element_to_be_clickable(e)).click()
                    break
                else:
                    sleep(2)
            file_name = get_downloaded_file_name(5, driver, tabs_handles)
            print("Download file")
    return file_name


def video_download(driver, message, wait, config_arr, tabs_handles):
    file_name = None
    if config_arr[1] == 1:
        size_string = message.find_element(By.CSS_SELECTOR, "div[class = 'im_message_body im_message_body_media']")\
            .find_element(By.CSS_SELECTOR, "div[class = 'im_message_document_info']")\
            .find_element(By.CSS_SELECTOR, "span[class = 'im_message_document_size ng-binding ng-scope']").text
        size = extract_size(size_string)

        if size <= config_arr[4]:
            element = wait.until(ec.element_to_be_clickable(
                message.find_element(By.CSS_SELECTOR, "div[class = "
                                                      "'im_message_video "
                                                      "im_message_document_thumbed "
                                                      "ng-scope']").find_elements(By.TAG_NAME, 'a')[1]))
            wait.until(ec.element_to_be_clickable(element.find_element(By.TAG_NAME, 'span'))).click()
            sleep(3)
            e = message.find_element(By.CSS_SELECTOR, "div[class ='im_message_document_actions noselect ng-scope']")
            while True:
                if e.find_element(By.CSS_SELECTOR,
                                  "span[class = 'nocopy ng-scope']").get_attribute("data-content") == "ذخیره":
                    wait.until(ec.element_to_be_clickable(e.find_elements(By.TAG_NAME, 'a')[1]
                                                          .find_element(By.TAG_NAME, 'span'))).click()
                    sleep(1)
                    break
                else:
                    sleep(1)

            file_name = get_downloaded_file_name(5, driver, tabs_handles)
            print("Download video")
    return file_name


def photo_download(driver, message, wait, config_arr, tabs_handles):
    caption = ""
    file_name = None
    if config_arr[0] == 1:
        sleep(2)

        # get photo caption
        try:
            caption = message.find_element(By.CSS_SELECTOR,
                                           "div[class = 'im_message_photo_caption"
                                           " ng-binding ng-scope']").text
        except Exception:
            pass

        for i in range(3):
            try:
                e = message.find_element(By.CSS_SELECTOR, "a[class ='im_message_photo_thumb']")
                wait.until(ec.element_to_be_clickable(e)).click()
                check_alert(driver)
                sleep(2)
                e1 = driver.find_element(By.CSS_SELECTOR, "a[class ='media_modal_action_btn']")
                wait.until(ec.element_to_be_clickable(e1)).click()
                sleep(2)
                wait.until(ec.element_to_be_clickable(driver.find_element(By.CSS_SELECTOR,
                                                                          "div[class ='modal_close_wrap "
                                                                          "modal_close_wrap_wnext ng-scope']"))).click()
                sleep(2)
                file_name = get_downloaded_file_name(5, driver, tabs_handles)
                print("Download photo")
                return file_name, caption
            except ElementClickInterceptedException:
                sleep(1)
                try:
                    # click on "بسیار خب"
                    driver.find_element(By.CSS_SELECTOR, "div[class = 'modal-dialog']").\
                        find_elements(By.TAG_NAME, "button").click()
                except Exception:
                    try:
                        driver.switch_to.alert().accept()
                        # print(" Alert accept worked!")

                    except Exception:
                        try:
                            # TODO
                            driver.switch_to.alert().dismiss()
                            # print(" Alert dismiss worked!")
                        except Exception:
                            try:
                                # TODO
                                driver.switch_to.alert().send_key(Keys.ENTER)
                                # print(" Alert Enter worked!")
                            except Exception:
                                pass

                finally:
                    # try to download
                    try:
                        sleep(3)
                        e1 = driver.find_element(By.CSS_SELECTOR, "a[class ='media_modal_action_btn']")
                        wait.until(ec.element_to_be_clickable(e1)).click()
                        sleep(2)
                        wait.until(ec.element_to_be_clickable(driver.find_element(By.CSS_SELECTOR,
                                                                                  "div[class ='modal_close_wrap "
                                                                                  "modal_close_wrap_wnext "
                                                                                  "ng-scope']"))).click()
                        sleep(2)
                        file_name = get_downloaded_file_name(5, driver, tabs_handles)
                        print("Download photo")

                        return file_name, caption
                    except Exception:
                        return "NULL", caption


def extract_size(size_string):
    try:
        size_m = size_string[-2:]
        if size_m == "GB":
            try:
                size = float(size_string[:-3]) * 1048576
            except ValueError:
                size = 0
            # print(size)
        elif size_m == "MB":
            try:
                size = float(size_string[:-3]) * 1024
            except ValueError:
                size = 0
            # print(size)
        elif size_m == "KB":
            try:
                size = float(size_string[:-3])
            except ValueError:
                size = 0
            # print(size)
        else:
            try:
                size = float(size_string[:-2]) * (1/1024)
            except ValueError:
                size = 0
            # print(size)
    except Exception:
        size = 0

    return size


def get_photos(driver, tabs_handles):
    file_name = ""
    try:
        wait = WebDriverWait(driver, 10)
        wait.until(ec.element_to_be_clickable(driver.find_element(
            By.CSS_SELECTOR, "[class = 'peer_modal_photo ng-scope peer_photo_init']"))).click()
        sleep(2)

        check_alert(driver)
        try:
            wait.until(ec.element_to_be_clickable(driver.find_element(
                By.CSS_SELECTOR, "a[class = 'media_modal_action_btn']"))).click()
            sleep(1)
            file_name = get_downloaded_file_name(5, driver, tabs_handles)
        except Exception:
            pass
        try:
            wait.until(ec.element_to_be_clickable(driver.find_element(
                By.XPATH, "/html/body/div[6]/div[3]"))).click()
        except Exception:
            close = driver.find_element(By.XPATH, "/html/body/div[6]")
            action = ActionChains(driver)
            action.move_to_element_with_offset(close, 20, 20)
            action.click()
            action.perform()
    except Exception:
        return "NULL"
    return file_name


# todo: try except
def get_profile_photos(driver, config_arr, tabs_handles):
    profiles = []
    try:
        wait = WebDriverWait(driver, 10)

        # check if this account has not any profile
        try:
            try:
                driver.find_element(By.CSS_SELECTOR, "span[class = 'peer_initials nocopy "
                                                     "peer_modal_photo user_bgcolor_7']")
                return profiles
            except NoSuchElementException:
                driver.find_element(By.XPATH, "/html/body/div[6]/div[2]/div/div/div[1]/div[2]/div[1]/a/span")
                return profiles
        except NoSuchElementException:
            pass

        # click on profiles button
        try:
            try:
                profile_button = driver.find_element(By.XPATH,
                                                     "/html/body/div[6]/div[2]/div/div/div[1]/div[2]/div[1]/a")
                driver.execute_script("arguments[0].click();", profile_button)
            except NoSuchElementException:
                wait.until(ec.element_to_be_clickable(driver.find_element(
                    By.XPATH, "/html/body/div[6]/div[2]/div/div/div[1]/div[2]/div[1]/a"))).click()
        except Exception:
            wait.until(ec.element_to_be_clickable(driver.find_element(
                By.CSS_SELECTOR, "a[class = 'peer_modal_photo peer_photo_init']"))).click()

        sleep(1)
        check_alert(driver)

        arr = driver.find_element(By.XPATH, "/html/body/div[7]/div[4]").\
            find_element(By.XPATH, "/html/body/div[7]/div[4]/div/div[3]/my-i18n").\
            find_elements(By.CLASS_NAME, "ng-binding")
        profiles_num = int(arr[-1].text)
        if config_arr[6] <= profiles_num:
            profiles_num = config_arr[6]

        download_profiles(driver, profiles_num, wait, tabs_handles)
        sleep(3)
        try:
            try:
                ActionChains(driver).click(driver.find_element(
                    By.XPATH, "/html/body/div[5]/div[1]")).perform()
            except Exception:
                b = driver.find_element_by_xpath("/html/body/div[5]/div[1]")
                driver.execute_script("arguments[0].click();", b)
                # wait.until(ec.element_to_be_clickable(driver.find_element(
                #     By.CSS_SELECTOR, "div[class = 'modal_close_wrap modal_close_wrap_wnext ng-scope']"))).click()
        except Exception:
            close = driver.find_element(By.XPATH, "/html/body/div[5]")
            action = ActionChains(driver)
            action.move_to_element_with_offset(close, 20, 20)
            action.click()
            action.perform()

        sleep(1)
        return profiles
    except Exception:
        return profiles


def download_profiles(driver, profiles_num, wait, tabs_handles):
    profiles = []
    try:
        for i in range(profiles_num):
            sleep(2)

            # download
            try:
                wait.until(ec.element_to_be_clickable(driver.find_element(By.XPATH, "/html/body/div[7]"
                                                                                    "/div[4]/div/div[1]/a[1]"))).click()
                sleep(2)
            except TimeoutException:
                download_button = driver.find_element(By.XPATH, "/html/body/div[7]/div[4]/div/div[1]/a[1]")
                driver.execute_script("arguments[0].click();", download_button)
                sleep(2)

            sleep(2)
            profiles.append(get_downloaded_file_name(5, driver, tabs_handles))

            # next
            try:
                try:
                    wait.until(ec.element_to_be_clickable(driver.find_element(
                        By.CSS_SELECTOR, "div[class = 'modal_prev_wrap ng-scope modal_prev_active_wrap']"))).click()
                    sleep(2)
                except TimeoutException:
                    next_button = driver.find_element(By.XPATH, "/html/body/div[6]/div[1]")
                    driver.execute_script("arguments[0].click();", next_button)
                    sleep(2)
            except Exception:
                pass
    except Exception:
        pass
    return profiles


def open_download(driver):
    driver.execute_script("window.open()")
    tabs_handles = driver.window_handles
    WebDriverWait(driver, 10).until(ec.new_window_is_opened)
    driver.switch_to.window(driver.window_handles[-1])
    driver.get("about:downloads")
    driver.switch_to.window(driver.window_handles[0])
    return tabs_handles


def get_downloaded_file_name(wait_time, driver, tabs_handles):
    driver.switch_to.window(tabs_handles[1])
    end_time = time() + wait_time
    while True:
        try:
            file_name = driver.execute_script("return document.querySelector"
                                              "('#contentAreaDownloadsView .downloadMainArea "
                                              ".downloadContainer description:nth-of-type(1)').value")
            if file_name:
                driver.switch_to.window(tabs_handles[0])
                sleep(3)
                return file_name
        except Exception:
            pass
        sleep(1)
        if time() > end_time:
            driver.switch_to.window(tabs_handles[0])
            sleep(3)
            return None


def check_alert(driver):
    try:
        WebDriverWait(driver, 5).until(ec.alert_is_present())
        alert = driver.switch_to.alert
        alert.accept()
        print("alert Exists in page")
    except Exception:
        pass
    sleep(1)

