import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

user = input("Please enter email of the user want to remove from rooms: ")

# from selenium.webdriver.firefox.options import Options
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
#options = webdriver.ChromeOptions()
#/home/paulnguyen/.config/google-chrome/ is profile that you work. Use it for Selenium may cause issue ==> make /userdata so that there is no confliction.
# options.add_argument("user-data-dir=/home/paulnguyen/.config/google-chrome/userdata")
# driver = webdriver.Chrome(executable_path="/home/paulnguyen/chromedriver_ChromeV85/chromedriver", options=options)
profile = webdriver.FirefoxProfile('/home/paulnguyen/.mozilla/firefox/paulnguyen/')
driver = webdriver.Firefox(profile)
#Below command need to Init Profile: https://stackoverflow.com/questions/37247336/selenium-use-of-firefox-profile
#options = Options()
#options.add_argument("-profile")
#options.add_argument("/home/paulnguyen/.mozilla/firefox/paulnguyen/")
#firefox_capabilities = DesiredCapabilities.FIREFOX
#firefox_capabilities['marionette'] = True
#driver = webdriver.Firefox(capabilities=firefox_capabilities, options=options)



#driver = webdriver.Firefox(executable_path="/home/paulnguyen/PycharmProjects/geckodriver_v0_27_0_ForFireFox_MinV60/geckodriver")

arrCONSTANT_ROOMCHAT = ["Room 1", "Room 2", "Room 3", "All Rooms"]
driver.get("https://chat.google.com/room/AAAAq4xJICA")
time.sleep(3)

driver.find_element_by_xpath("//div[text()='More rooms.']//parent::div").click()
time.sleep(3)

def remove_user_from_room(room_name, user):
    room_xpath = "//span[text()='" + room_name + "']"
    try:
        driver.find_element_by_xpath(room_xpath).click()
        bRoomExist = "Y"
    except Exception as e:
        print("Room {} not found".format(room_name))
        bRoomExist = "N"

    if bRoomExist == "Y":
        time.sleep(3)

        driver.find_element_by_xpath("//span[@class='wWf0Bc ojqkvd']/parent::span/parent::span").click()
        time.sleep(3)

        driver.find_element_by_css_selector("div[data-item='members']").click()
        time.sleep(3)

        try:
            driver.find_element_by_xpath("//span[text()='" + user + "']").click()
            bUserExist = 'Y'
        except Exception as e:
            print("User {} is not a member of room {}".format(user, room_name))
            bUserExist = 'N'

        if bUserExist == 'Y':
            driver.find_element_by_xpath("//span[@aria-label='" + user + "']/parent::div/parent::div/following-sibling::div/div").click()

            elements = driver.find_elements_by_xpath("//div[@data-item='remove']") # instead of elements 'message'
            for i in range(0, len(elements), 1):
                if elements[i].is_displayed():
                    # print("Element {} is displayed".format(i))
                    elements[i].click()
                    time.sleep(3)
                    try:
                        elements[i].click() # to make sure user is deleted.
                    except Exception as e:
                        print("Something wrong")
                    print("User {} has been removed from room {}".format(user, room_name))
                    break
        else:
            print("User is not removed")
            driver.find_element_by_xpath("//div[@class='g3VIld qRVtHc SrW2Bd Up8vH Whe8ub hFEqNb J9Nfi iWO5td']").send_keys(Keys.ESCAPE)
            time.sleep(3)



for room in arrCONSTANT_ROOMCHAT:
    remove_user_from_room(room, user)

time.sleep(5)
driver.close()