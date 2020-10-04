import time
from selenium import webdriver

user = input("User: ")
print("1. Project     ")
print("2. Product     ")
print("3. Design     ")
sTeam = input("Which team: ")

options = webdriver.ChromeOptions()
#/home/paulnguyen/.config/google-chrome/ is profile that you work. Use it for Selenium may cause issue ==> make /userdata so that there is no confliction.
options.add_argument("user-data-dir=/home/paulnguyen/.config/google-chrome/userdata")
driver = webdriver.Chrome(executable_path="/home/paulnguyen/chromedriver_ChromeV85/chromedriver", options=options)

arrCONSTANT_PROJECT = ["Room 1", "Room 2", "Room 3"]

arrCONSTANT_PRODUCT = ["Room 4", "Room 5", "Room 6"]

arrCONSTANT_DESIGN = ["Room 2", "Room 3", "Room 5"]

driver.get("https://chat.google.com/room/AAAAq4xJICA")
time.sleep(3)

driver.find_element_by_xpath("//div[text()='More rooms.']//parent::div").click()
time.sleep(3)

def add_user_to_room(room_name, user_email):
    room_xpath = "//span[text()='" + room_name + "']"
    try:
        driver.find_element_by_xpath(room_xpath).click()
        bRoomExist = "Y"
    except Exception as e:
        print("Room {} not found".format(room_name))
        bRoomExist = "N"

    if bRoomExist == "Y":
        time.sleep(3)

        driver.find_element_by_xpath("//span[@class='wWf0Bc ojqkvd']//parent::span//parent::span").click()
        time.sleep(3)

        driver.find_element_by_css_selector("div[data-item='invite']").click()
        time.sleep(3)
        driver.find_element_by_xpath("//label[text()='Notify people via email']//parent::label//parent::div").click()
        time.sleep(3)

        driver.find_element_by_css_selector("input[aria-label='Enter name or email of person or group']").send_keys(user_email)
        time.sleep(5)

        try:
            driver.find_element_by_css_selector("div[class='zsIcid L3gUle gVTkH']").click()
            time.sleep(2)
        except Exception as e:
            print("User {} is already a member of the group or user not exist".format(user_email))
            driver.find_element_by_xpath("// span[text() = 'Cancel']").click()

        domain1_email = user_email.split("@")[0] + "@domain1.com"
        domain_alias_email = user_email.split("@")[0] + "@domain_alias.com"

        try:
            correct_selection = selected_user = driver.find_element_by_css_selector("div[data-hovercard-id='" + domain1_email + "']").is_displayed()
        except Exception as e:
            try:
                correct_selection = driver.find_element_by_css_selector("div[data-hovercard-id='" + domain_alias_email + "']").is_displayed()
            except Exception as e:
                correct_selection = 0
        if correct_selection:
            print("user {} has been added successfully to room {}".format(user_email, room_name))
            driver.find_element_by_xpath("// span[text() = 'Add']").click()
        else:
            print("Some thing wrong!!! \n User {} and room {}".format(user_email, room_name))
            driver.find_element_by_xpath("// span[text() = 'Cancel']").click()

def get_rooms(sTeam):
    switcher = {
        '1': arrCONSTANT_PROJECT,
        '2': arrCONSTANT_PRODUCT,
        '3': arrCONSTANT_DESIGN,
    }
    return switcher.get(sTeam, [])

arrRooms = get_rooms(sTeam)
print("Add user {} to rooms {}".format(user, arrRooms))

for room in arrRooms :
     add_user_to_room(room, user)

time.sleep(5)
driver.close()



