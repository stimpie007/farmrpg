import time
import secrets  # secrets.py file which contains credentials
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, \
    ElementNotInteractableException, StaleElementReferenceException


class FarmRpgFisher():

    def __init__(self, sleep_spacer=4):
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        self.sleep_spacer = sleep_spacer

        self.CATCH_FISH_LENGTH = 2.5
        self.FISHING_SPOT_COORDS = (11, 12, 13, 14, 21, 22, 23, 24, 31, 32, 33, 34)

    def quit(self) -> None:
        self.driver.quit()

    def login(self, username: str, password: str) -> None:
        self.driver.get('https://farmrpg.com/index.php#!/login.php')

        username_box = self.driver.find_element(By.NAME, 'username')
        username_box.clear()
        username_box.send_keys(username)

        pw_box = self.driver.find_element(By.NAME, 'password')
        pw_box.clear()
        pw_box.send_keys(password)

        pw_box.send_keys(Keys.RETURN)

        time.sleep(self.sleep_spacer)

    def navigate_to_fishing_spot_from_home(self, fishing_spot_id: int) -> None:
        general_fishing_link = self.driver.find_element(By.XPATH, f'//a[@href="fish.php"]')
        general_fishing_link.click()

        time.sleep(self.sleep_spacer)
        fishing_spot_link = self.driver.find_element(By.XPATH, f'//a[@href="fishing.php?id={fishing_spot_id}"]')
        fishing_spot_link.click()

        time.sleep(self.sleep_spacer)

    def fish(self, final_bait_count: int = 0) -> None:
        fishing_start_time = time.time()
        while self._get_bait_amount_left() > 0:
            try:
                fish = self.driver.find_element(By.XPATH, f'//img[contains(@class, "catch")]')
                fish.click()

                self._click_on_moving_blue_dot()

            except (NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException):
                continue

            time.sleep(.1)

    def _click_on_moving_blue_dot(self) -> None:
        # blue dot is 50x50 div and it lives on the very left
        # surrounding box is 300x50
        catch_start_time = time.time()
        blue_dot = self.driver.find_element(By.XPATH, f'//div[@class="fc"]')
        while time.time() - catch_start_time < self.CATCH_FISH_LENGTH:

            try:
                # blue_dot = driver.find_element(By.XPATH, f'//div[@class="fishcaught finalcatch2b"]')
                blue_dot.click()
            except (NoSuchElementException, ElementNotInteractableException) as e:
                pass

            time.sleep(.01)

    def _get_bait_amount_left(self) -> int:
        while True:
            try:
                text = self.driver.find_element(By.XPATH, '//*[@id="baitarea"]/div[1]/div[1]/strong').text
                return int(text)
            except:
                continue


if __name__ == '__main__':
    USERNAME = secrets.username
    PASSWORD = secrets.password

    fisher = FarmRpgFisher()
    fisher.login(USERNAME, PASSWORD)
    fisher.navigate_to_fishing_spot_from_home(8)

    fisher.fish()
    fisher.quit()
