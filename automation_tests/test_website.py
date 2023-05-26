import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture
def driver():
    # Set up the WebDriver
    driver = webdriver.Chrome()
    yield driver
    # Tear down the WebDriver
    driver.quit()


@pytest.fixture()
def go_to_plan_page(driver):
    driver.get("http://localhost:5173/")

    # Find an element and perform an action
    destination = driver.find_element(By.CLASS_NAME, "multiselect")
    destination.click()

    option = driver.find_element(By.CLASS_NAME, "multiselect__option")
    option.click()

    datepicker = driver.find_element(By.XPATH, './/*[@aria-label="Datepicker input"]')
    datepicker.click()

    first_date = driver.find_element(By.XPATH, './/*[text()="24"]')
    second_date = driver.find_element(By.XPATH, './/*[text()="25"]')

    first_date.click()
    second_date.click()

    select_button = driver.find_element(By.XPATH, './/*[text()="Select" ]')
    select_button.click()

    search_button = driver.find_element(By.XPATH, './/*[text()=" Search " ]')
    search_button.click()

    wait = WebDriverWait(driver, 10)
    wait.until(EC.url_contains('plan'))

    yield driver

    driver.quit()


def test_planning_page_opens(go_to_plan_page):
    # Open a webpage

    assert go_to_plan_page.current_url == "http://localhost:5173/plan"


def test_suggest_button_inactive(go_to_plan_page):
    # Open a webpage
    driver = go_to_plan_page
    suggest_trip_btn = driver.find_element(By.XPATH, './/*[text()=" Suggest trip " ]')

    assert not suggest_trip_btn.is_enabled()


def test_budget_edit_dialog_opens(go_to_plan_page):
    driver = go_to_plan_page
    pencil = driver.find_element(By.CLASS_NAME, "planning-heading-date-form-pencil-icon")
    pencil.click()

    assert EC.presence_of_element_located((By.CLASS_NAME, "planning-budget-container-popup overlay-content"))


def test_add_remove_budget_entry(go_to_plan_page):
    driver = go_to_plan_page
    pencil = driver.find_element(By.CLASS_NAME, "planning-heading-date-form-pencil-icon")
    pencil.click()

    add_entries = driver.find_element(By.CLASS_NAME, "planning-budget-container-popup-budget-entries-label")
    add_entries.click()
    assert EC.presence_of_element_located((By.CLASS_NAME, "planning-budget-container-popup-budget-entries"))

    close_btn = driver.find_element(By.CLASS_NAME, "planning-budget-container-popup-budget-entries-close")
    close_btn.click()

    assert EC.invisibility_of_element_located((By.CLASS_NAME, "planning-budget-container-popup-budget-entries"))


def test_budget_updates(go_to_plan_page):
    driver = go_to_plan_page
    pencil = driver.find_element(By.CLASS_NAME, "planning-heading-date-form-pencil-icon")
    pencil.click()

    add_entries = driver.find_element(By.CLASS_NAME, "planning-budget-container-popup-budget-entries-label")
    add_entries.click()

    amount_input = driver.find_element(By.XPATH, './/*[@placeholder="Enter amount"]')
    amount_input.clear()
    amount_input.send_keys("100")

    entry_amount_input = driver.find_element(By.XPATH, "//div[@class='planning-budget-container-popup-budget-entries']//input[@placeholder='Enter amount']")
    entry_amount_input.send_keys("100")

    save_btn = driver.find_element(By.XPATH, './/*[text()=" Save " ]')

    assert save_btn.is_enabled()
    save_btn.click()

    label = driver.find_element(By.XPATH, "//div[contains(@class, 'planning-budget-container')]//h3")

    assert label.text == 'Your budget - 100 $'


def test_place_added(go_to_plan_page):
    driver = go_to_plan_page
    add_place = driver.find_element(By.CLASS_NAME, "planning-daily-activity-add-place")
    add_place.click()
    place_input = driver.find_element(By.CLASS_NAME, "multiselect")
    place_input.click()

    option = driver.find_element(By.CLASS_NAME, "multiselect__option")
    option.click()

    assert EC.presence_of_element_located((By.CLASS_NAME, "planning-daily-activity-card"))


def test_place_removed(go_to_plan_page):
    driver = go_to_plan_page
    add_place = driver.find_element(By.CLASS_NAME, "planning-daily-activity-add-place")
    add_place.click()
    place_input = driver.find_element(By.CLASS_NAME, "multiselect")
    place_input.click()

    option = driver.find_element(By.CLASS_NAME, "multiselect__option")
    option.click()

    remove_icon = driver.find_element(By.CLASS_NAME, "planning-daily-activity-remove")
    driver.execute_script("arguments[0].click();", remove_icon)

    assert EC.invisibility_of_element_located((By.CLASS_NAME, "planning-daily-activity-card"))


def test_login_dialog_opens(driver):
    driver.get("http://localhost:5173/")
    login_btn = driver.find_element(By.XPATH, './/*[text()="Login"]')
    login_btn.click()
    assert EC.presence_of_element_located((By.CLASS_NAME, "home-welcome-auth overlay-content"))


def test_sign_up_dialog_opens(driver):
    driver.get("http://localhost:5173/")
    login_btn = driver.find_element(By.XPATH, './/*[text()="SignUp"]')
    login_btn.click()
    assert EC.presence_of_element_located((By.CLASS_NAME, "home-welcome-auth-sign-up overlay-content"))


def test_sign_up_dialog_opens_after_clicking_register_on_login(driver):
    driver.get("http://localhost:5173/")
    login_btn = driver.find_element(By.XPATH, './/*[text()="Login"]')
    login_btn.click()
    login_btn = driver.find_element(By.XPATH, './/*[text()="Register"]')
    login_btn.click()
    assert EC.presence_of_element_located((By.CLASS_NAME, "home-welcome-auth-sign-up overlay-content"))