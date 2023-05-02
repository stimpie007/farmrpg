import time
import secrets  # secrets.py file which contains credentials
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, \
    StaleElementReferenceException


class FarmRpgExplorer:

    def __init__(self, sleep_spacer=1):
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()
        self.sleep_spacer = sleep_spacer

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

    def navigate_to_explore_spot_from_home(self, explore_spot_id: int) -> None:
        time.sleep(2)
        general_explore_link = self.driver.find_element(By.XPATH, f'//a[@href="explore.php"]')
        general_explore_link.click()

        time.sleep(self.sleep_spacer)

        explore_spot_link = self.driver.find_element(By.XPATH, f'//a[@href="area.php?id={explore_spot_id}"]')
        explore_spot_link.click()

        time.sleep(self.sleep_spacer)

    def explore(self) -> None:
        while self._get_sprint_amount_left() > 0:
            try:
                continue_exploring = self.driver.find_element(By.XPATH, f'//div[contains(@class, "explorebtn")]')
                continue_exploring.click()

            except (NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException):
                continue

            time.sleep(.1)

        continue_exploring = self.driver.find_element(By.XPATH, f'//a[@href="index.php"]')
        continue_exploring.click()

        time.sleep(self.sleep_spacer)

    def _get_sprint_amount_left(self) -> int:
        while True:
            try:
                text = self.driver.find_element(By.XPATH, '//*[@id="stamina"]').text
                return int(text)
            except:
                continue


if __name__ == '__main__':
    USERNAME = secrets.username
    PASSWORD = secrets.password

    explorer = FarmRpgExplorer()
    explorer.login(USERNAME, PASSWORD)
    explorer.navigate_to_explore_spot_from_home(4)

    explorer.explore()
    explorer.quit()
