import time
import config
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, \
    StaleElementReferenceException, ElementNotInteractableException


def login():
    driver.get('https://farmrpg.com/index.php#!/login.php')

    username_box = driver.find_element(By.NAME, 'username')
    username_box.clear()
    username_box.send_keys(config.USERNAME)

    pw_box = driver.find_element(By.NAME, 'password')
    pw_box.clear()
    pw_box.send_keys(config.PASSWORD)

    pw_box.send_keys(Keys.RETURN)

    time.sleep(sleep_timer)


def run_daily_tasks():
    # TODO: Remove repetitiveness; Command pattern?
    # Farm harvest and plant all
    driver.get(f'https://farmrpg.com/#!/xfarm.php?id={config.FARM_ID}"')
    time.sleep(sleep_timer)
    driver.find_element(By.CLASS_NAME, 'harvestallbtn').click()
    time.sleep(sleep_timer)
    driver.find_element(By.CLASS_NAME, 'plantallbtn').click()
    time.sleep(sleep_timer)

    # Chiken coop pet all
    driver.find_element(By.XPATH, f'//a[contains(@href, "coop.php?id={config.FARM_ID}")]').click()
    time.sleep(sleep_timer)
    driver.find_element(By.CLASS_NAME, 'petallbtn').click()
    time.sleep(sleep_timer)
    driver.find_element(By.CLASS_NAME, 'modal-button-bold').click()
    time.sleep(sleep_timer)

    # Cow pasture pet all
    # driver.find_element(By.XPATH, f'//a[contains(@href, "pasture.php?id={config.FARM_ID}")]').click()
    time.sleep(sleep_timer)
    driver.find_element(By.CLASS_NAME, 'petallbtn').click()
    time.sleep(sleep_timer)
    driver.find_element(By.CLASS_NAME, 'modal-button-bold').click()
    time.sleep(sleep_timer)

    # Storehouse do some work
    # driver.find_element(By.XPATH, f'//a[contains(@href, "storehouse.php?id={config.FARM_ID}")]').click()
    time.sleep(sleep_timer)
    driver.find_element(By.CLASS_NAME, 'workbtnnc').click()
    time.sleep(sleep_timer)
    driver.find_element(By.CLASS_NAME, 'modal-button-bold').click()
    time.sleep(sleep_timer)


def go_explore(explore_area='Forest'):
    explore_id = {
        'Forest': 7,
        'Small Cave': 1,
        'Small Spring': 2,
        'Highland Hills': 3,
        'Cane Pole Ridge': 4,
        'Misty Forest': 5,
        'Black Rock Canyon': 6
    }[explore_area]

    driver.get(f'https://farmrpg.com/#!/area.php?id={explore_id}')
    time.sleep(sleep_timer)
    continue_btn = driver.find_element(By.XPATH, f'//div[contains(@class, "explorebtn")]')

    # Explore
    while _get_sprint_amount_left() > 0:
        try:
            continue_btn.click()
        except (NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException):
            continue

        time.sleep(.1)


def _get_sprint_amount_left() -> int:
    while True:
        try:
            text = driver.find_element(By.XPATH, '//*[@id="stamina"]').text
            return int(text)
        except:
            continue


def go_fishing(fishing_pond='Farm Pond'):
    fishing_id = {
        'Farm Pond': 2,
        'Small Pond': 1,
        'Forest Pond': 3,
        'Lake Tempest': 4,
        'Small Island': 5,
        'Crystal River': 6,
        'Emerald Beach': 7
    }[fishing_pond]

    driver.get(f'https://farmrpg.com/#!/fishing.php?id={fishing_id}')
    time.sleep(sleep_timer)

    while _get_bait_amount_left() > 0:
        try:
            driver.find_element(By.CLASS_NAME, 'catch').click()
            _click_on_moving_blue_dot()

        except (NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException):
            continue

        time.sleep(.1)


def _click_on_moving_blue_dot() -> None:
    # blue dot is 50x50 div and it lives on the very left
    # surrounding box is 300x50
    catch_start_time = time.time()
    blue_dot = driver.find_element(By.XPATH, f'//div[@class="fc"]')
    while time.time() - catch_start_time < 2.5:

        try:
            # blue_dot = driver.find_element(By.XPATH, f'//div[@class="fishcaught finalcatch2b"]')
            blue_dot.click()
        except (NoSuchElementException, ElementNotInteractableException):
            pass

        time.sleep(.01)


def _get_bait_amount_left() -> int:
    while True:
        try:
            text = driver.find_element(By.XPATH, '//*[@id="baitarea"]/div[1]/div[1]/strong').text
            return int(text)
        except:
            continue


def logout():
    driver.get('https://farmrpg.com/index.php#!/logout.php')
    time.sleep(sleep_timer)
    driver.find_element(By.CLASS_NAME, 'logoutlink').click()


if __name__ == "__main__":
    # Setup
    driver = webdriver.Firefox()
    driver.maximize_window()

    sleep_timer = 3

    # Actions
    login()
    run_daily_tasks()
    go_explore('Black Rock Canyon')
    go_fishing('Small Pond')
    logout()

    driver.quit()
