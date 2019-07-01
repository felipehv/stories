import lxml
import requests
from selenium import webdriver as wd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
import datetime
from time import sleep
import json
import os
import pickle

env = os.getenv('pyenv')
class StoriesWD():

    def __init__(self):
        """
        chrome_options will decide if showing
        the GUI or not.
        """
        chrome_options = wd.ChromeOptions()
        # mobile_emulation = { "deviceName": "iPhone X" }
        # chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
        if env == 'production':
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
        self.driver = wd.Chrome('./chromedriver', options=chrome_options)

    def login(self, user, password):
        """
        If cookies are already stored, try
        loading them. Else, it will try to
        login and then save them.
        """
        self.driver.get("https://www.instagram.com/accounts/login/")
        sleep(2)
        user_field = self.driver.find_element_by_name("username")
        pass_field = self.driver.find_element_by_name("password")
        user_field.send_keys(user)
        pass_field.send_keys(password)
        pass_field.send_keys(Keys.RETURN)

    def load_cookies(self):
        self.driver.get('https://www.instagram.com/')
        if "cookies.pkl" in os.listdir("./"):
            cookies = pickle.load(open("cookies.pkl", "rb"))
            for cookie in cookies:
                self.driver.add_cookie(cookie)
        print("Successfully loaded cookies")      

    def save_cookies(self):
        pickle.dump( self.driver.get_cookies() , open("cookies.pkl","wb"))
        print("Successfully saved cookies")      

    def home(self):
        self.driver.get("https://www.instagram.com/huaweimobilecl/")
        sleep(2)

    def get_user(self,username):
        self.driver.get(f"https://www.instagram.com/{username}/")
        sleep(2)

    def stories(self, force=False):
        images=[]
        videos=[]
        try:
            dimension = int(self.driver.find_element_by_class_name("CfWVH").get_attribute("height"))
        except Exception as e:
            print("No stories at the time")
            return images, videos
        if dimension % 168 != 0 and not force:
            return images, videos

        story_button = self.driver.find_element_by_class_name("_6q-tv")
        story_button.click()
        sleep(1)
        while True:
            react_root = self.driver.find_element_by_id("react-root")
            section = react_root.find_elements_by_class_name("_9eogI")[0]
            section_class_size = len(section.get_attribute("class").split(" "))
            if section_class_size > 2:
                video_url = None
                try:
                    video = section.find_element_by_css_selector("div video source")
                    video_url = video.get_attribute("src")
                    # print(f"Video URL: {video_url}")
                    videos.append(video_url)
                except Exception as e:
                    print("No video found")
                finally:
                    image = section.find_element_by_css_selector("img.y-yJ5")
                    image_url = image.get_attribute("src")
                    # print(f"Screenshot: {image_url}")
                    if video_url is None:
                        images.append(image_url)
            else:
                print("End of Stories")
                return images, videos
            next_button = section.find_element_by_class_name("coreSpriteRightChevron")
            next_button.click()
            sleep(1)

            return images, videos

    def download_stories(self, username, force=False):
        """
        Goes to :username: profile and gets
        all urls.
        """
        self.get_user(username)
        return self.stories(force)
            
    def take_screenshot(self, name):
        self.driver.save_screenshot(f"{name}.png")

    def close(self):
        self.driver.close()

if __name__ == "__main__":
    scraper = StoriesWD()
    scraper.load_cookies()
    print(scraper.download_stories("ignaciosoffia", force=True))
    scraper.save_cookies()
    scraper.close()
    # scraper.login('citizenpixel', '1997igna')
